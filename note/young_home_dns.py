# -*- coding: utf-8 -*-
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkecs.request.v20140526 import DescribeInstancesRequest
from aliyunsdkecs.request.v20140526 import StopInstanceRequest

# Initialize AcsClient instance
client = AcsClient(
    "LTAI9y8Ix2SUJoKP",
    "kkYyYuOo1JUkU5enCOlp1TbCzIDpnx",
    # "<your-region-id>"
);

# Initialize a request and set parameters
request = DescribeInstancesRequest.DescribeInstancesRequest()
request.set_PageSize(10)

# Print response
response = client.do_action_with_exception(request)
print response