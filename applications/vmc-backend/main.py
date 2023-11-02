# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import json
import logging
import re
import os
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer

api_token = os.getenv("VMC_API_TOKEN")
org_id = os.getenv("VMC_ORG_ID")
sddc_id = os.getenv("VMC_SDDC_ID")
VMC_AUTH_URL = "https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize?refresh_token={}".format(api_token)
VMC_SDDC_SUMMARY_URL = "https://vmc.vmware.com/vmc/api/orgs/{}/sddcs/{}".format(org_id, sddc_id)

# Press the green button in the gutter to run the script.
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if re.search('/vmc', self.path):
            # Get auth token
            auth_response = requests.post(VMC_AUTH_URL).json()
            token = auth_response.get("access_token")
            logger.info(token)

            # Get SDDC summary
            headers = {"Content-Type": "application/json", "csp-auth-token": token}
            summary_response = requests.get(VMC_SDDC_SUMMARY_URL, headers=headers).json()
            sddc_name = summary_response.get("name")
            sddc_version = summary_response.get("resource_config").get("sddc_manifest").get("vmc_version")
            create_date = summary_response.get("created")
            deployment_type = summary_response.get("resource_config").get("deployment_type")
            region = summary_response.get("resource_config").get("region")
            availability_zone = summary_response.get("resource_config").get("availability_zones")
            instance_type = summary_response.get("resource_config").get("sddc_manifest").get("esx_ami").get("instance_type")
            logger.info("sddc_name: {}\nsddc_version: {}\ncreate_date: {}\ndeployment_type:{}\nregion:{}\navailability_zone: {}\ninstance_type: {}"
                        .format(sddc_name, sddc_version, create_date, deployment_type, region, availability_zone, instance_type))

            # message = {
            #     "sddc_name": "{}".format(sddc_name),
            #     "sddc_version": "{}".format(sddc_version),
            #     # "create_date": "{}".format(create_date),
            #     # "deployment_type": "{}".format(deployment_type),
            #     "region": "{}".format(region),
            #     "availability_zone": "{}".format(availability_zone[0]),
            #     "instance_type": "{}".format(instance_type)
            # }
            message = "SDDC Name: {}, SDDC Version: {}, Region: {}, Instance Type: {}".format(sddc_name, sddc_version, region, instance_type)

            # send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            # self.wfile.write(json.dumps(message).encode("utf-8"))
            self.wfile.write(message.encode("utf-8"))
        elif re.search('/', self.path):
            self.send_response(200, "The server is health")
        else:
            self.send_response(403, "Not Found")
        self.end_headers()


if __name__ == '__main__':
    logger = logging.getLogger()
    logging.basicConfig(level=logging.INFO)
    logger.info('Starting server...')
    server = HTTPServer(("0.0.0.0", 3000), HTTPRequestHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    logging.info('Stopping httpd...\n')
