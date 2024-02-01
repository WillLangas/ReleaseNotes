import requests
import base64
import sys
import re

class DevOpsHandler:
    """
    The class for handling all requests to the Azure DevOps service through the REST API. Allows 
    the user to validate their connection to the project, and also execute querys on work item 
    lists
    """    

    def __init__(self, organization, project, encoded_pat):
        """
        The constructor for a DevOpsHandler object. Sets the class fields to their intialized
        values, and also builds the headers dictionary that will be used when sending requests
        to the Azure DevOps REST API

        Args:
            organization (str): The organization name in DevOps
            project (str): The project name in DevOps
            encoded_pat (str): The base64 encoded value of the user's personal access token
        """
        self.organization = organization
        self.project = project
        self.org_url = f"https://dev.azure.com/{self.organization}/{self.project}"

        self.encoded_pat = encoded_pat
        
        # Build out the headers dictionary with the return type for requests, and PAT information
        self.headers = {
            'Content-Type': 'application/json-patch+json',
            'Authorization': f'Basic {self.encoded_pat}'
        }
    
    def getWorkItems(self, query_ID):
        """
        Calls the provided query, and returns a list of all the ID for each work item that is 
        provided as a result. Uses the _buildIDListHelper in order to retrieve the ID
        values.

        Args:
            query_ID (str): An ID string for the query to retrieve work items marked for release

        Raises:
            Exception: In the case that the DevOps API request fails, raise an exception

        Returns:
            [int]: A list of retrieved work item IDs
        """
        base_url = f"{self.org_url}/_apis/wit/wiql/{query_ID}?api-version=7.1"

        response = requests.get(base_url, headers=self.headers)

        if response.status_code == 200:
            query_results = response.json()
        else:
            raise Exception("Failure to execute initial query properly")
        

        work_item_IDs = self._buildIDListHelper(query_results)

        return work_item_IDs
    
    def _buildIDListHelper(self, query_results):
        """
        Helper function used for taking the results of the query execution, and iterating through
        the resulting work items, pulling out the ID of each item and returning the list

        Args:
            query_results (dict): The results of a query call to the REST API

        Returns:
            [int]: A list of work item IDs as int literals
        """
        work_item_IDs = []

        # When the work items are returned as workItemLinks the ID is extracted from a different field
        if query_results['queryResultType'] == 'workItemLink': 
            for item in query_results['workItemRelations']:
                work_item_IDs.append(item['target']['id'])
        elif query_results['queryResultType'] == 'workItem':
            for item in query_results['workItems']:
                work_item_IDs.append(item['id'])

        return work_item_IDs
    
    def gatherWorkItemDescriptions(self, work_item_IDs):
        """
        Using the list of work item IDs, retrieve the corresponding work item title and description
        for each work item on the list. Return the list of these work item dictionaries.

        Args:
            work_item_IDs ([int]): A list of work item IDs as int literals

        Returns:
            [{dict}]: A list of work items represented as dictionaries with a title and description
        """

        results = []
        for ID in work_item_IDs:

            # Retrieve the work item using the DevOps API
            base_url = f'https://dev.azure.com/getnerdio/NMW/_apis/wit/workitems/{ID}?api-version=7.1'
            response = requests.get(base_url, headers=self.headers).json()
            
            # Format the temporary dictionary used to store title and description
            work_item = {}
            work_item['Title'] = response['fields']['System.Title']
            work_item['ID'] = ID
            work_item['Description'] = response['fields']['System.Description']

            results.append(work_item)
        
        return results
