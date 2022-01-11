from aws_cdk import Stack, CfnOutput
from static_site import StaticSitePrivateS3


class StaticSiteStack(Stack):
    def __init__(self, scope, construct_id, props, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        site = StaticSitePrivateS3(
            self,
            f"{props['namespace']}-construct",
            domain_name=props["domain_name"]
        )

        CfnOutput(
            self,
            "SiteBucketName",
            value=site.bucket.bucket_name,
        )
        CfnOutput(
            self,
            "DistributionId",
            value=site.distribution.distribution_id,
        )
        CfnOutput(
            self,
            "CertificateArn",
            value=site.certificate.certificate_arn,
        )
