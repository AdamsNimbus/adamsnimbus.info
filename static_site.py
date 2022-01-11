"""
Two constructs to host static sites in aws using S3, cloudfront and Route53.
"""
from aws_cdk import (
    aws_s3 as s3,
    aws_s3_deployment as s3_deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as targets,
    RemovalPolicy
)
from constructs import Construct

class StaticSite(Construct):
    """The base class for StaticSite constructs"""

    def __init__(
        self,
        scope,
        construct_id,
        domain_name,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        # Public variables
        self.bucket = None
        self.certificate = None
        self.distribution = None

        # Instance Variables
        self._domain_name = domain_name

    def _build_site(self):
        """The Template Method for building the site.

        It uses hook functions which are implemented in the sub classes
        """
        # Create the S3 bucket for the site contents
        self._create_site_bucket()

        self._deploy_site()

        # Get the hosted zone based on the provided domain name
        hosted_zone = self.__create_hosted_zone()

        # Get an existing or create a new certificate for the site domain
        self.__create_certificate(hosted_zone)

        # create the cloud front distribution
        self._create_cloudfront_distribution()

        # Create a Route53 record
        self.__create_route53_record(hosted_zone)

    def _create_site_bucket(self):
        """a virtual function to be implemented by the sub classes"""

    def _deploy_site(self):
        """a virtual function to be implemented by the sub classes"""

    def _create_cloudfront_distribution(self):
        """a virtual function to be implemented by the sub classes"""

    def __create_hosted_zone(self):
        return route53.HostedZone(
            self,
            "hosted_zone",
            zone_name=self._domain_name,
            comment="Hosted zone for the static site",
        )

    def __create_route53_record(self, hosted_zone):
        route53.ARecord(
            self,
            "site-alias-record",
            record_name=self._domain_name,
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                targets.CloudFrontTarget(self.distribution)
            ),
        )

    def __create_certificate(self, hosted_zone_id):
        self.certificate = acm.DnsValidatedCertificate(
            self,
            "site_certificate",
            domain_name=self._domain_name,
            hosted_zone=hosted_zone_id,
            region="us-east-1",
        )


class StaticSitePrivateS3(StaticSite):
    def __init__(
        self,
        scope,
        construct_id,
        **kwargs,
    ):
        super().__init__(scope, construct_id, **kwargs)

        self._build_site()

    def _create_site_bucket(self):
        """Creates a private S3 bucket for the static site construct"""
        self.bucket = s3.Bucket(
            self,
            "site_bucket",
            bucket_name=self._domain_name,
            encryption=s3.BucketEncryption.S3_MANAGED,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

    def _deploy_site(self):
        """Deploy the site to the bucket"""
        self.deployment = s3_deploy.BucketDeployment(self, "DeployWebsite",
            sources=[s3_deploy.Source.asset("./src")],
            destination_bucket=self.bucket,
        )

    def _create_cloudfront_distribution(self):
        """Create a cloudfront distribution with a private bucket as the origin"""


        self.distribution = cloudfront.Distribution(
            self,
            "cloudfront_distribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(self.bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
            ),
            domain_names=[self._domain_name],
            certificate=self.certificate,
            default_root_object="index.html",
        )
