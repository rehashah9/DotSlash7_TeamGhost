import requests
from bs4 import BeautifulSoup

def scrap_steampipe(url, response):
    # Send a GET request to the URL
    target_id = "table-usage-guide"
    
    table_content = ""
    # file_name = url.split("/")[-1]
    # data_file = open(f"./{file_name}.txt", "w")
    table_content+="Examples for SQL Queries & their Use Case for Table: \n\n"
    # data_file.write(f"Examples for SQL Queries & their Use Case for Table: {file_name}\n\n")
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
    # Parse the HTML content of the page using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the target element by ID
        start_element = soup.find(id="table-usage-guide")
        end_element = soup.find(id="query-examples")
        if end_element == None:
            ## Find the target element by class
            end_element = soup.find(id="inspect")

        if start_element and end_element:
            # Extract content between the start and end elements
            content_between = ''.join(str(tag) for tag in start_element.find_all_next() if tag != end_element)
            content_soup = BeautifulSoup(content_between, 'html.parser')

            # Print or process the content
            h3_elements = content_soup.find_all('h3')

            # Print or process the <h3> elements
            # print("Found <h3> elements between the specified IDs:")
            for h3_element in h3_elements:
                # print(h3_element.text.strip())
                table_content+="Query Name: " + h3_element.text.strip() + "\n"
                # data_file.write(f"{h3_element.text.strip()}: \n")

                p_element = h3_element.find_next('p')
                if p_element:
                    # print("p:", p_element.text.strip())
                    table_content+="Query Meaning: " + p_element.text.strip() + "\n"
                    # data_file.write(f"Description: {p_element.text.strip()}\n")

                # Find the immediately following <code> block
                code_block = h3_element.find_next('code')
                if code_block:
                    # print("code:", code_block)
                    code_content = ' '.join(code_block.stripped_strings)
                    table_content+="SQL Query: " + code_content + "\n"

                    # data_file.write(f"SQL Query: {code_content}\n")


                # print("----")
                # data_file.write("----\n")
                table_content+="\n"

        else:
            print(f"One or both of the specified IDs not found.")

    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")


    return table_content


def scrap_schema_for_table(url,response):
    table_content = ""

    ## Get the Title
    file_name = url.split("/")[-1]
    soup = BeautifulSoup(response.content, 'html.parser')
    data_file = open(f"./{file_name}.txt", "w")
    # data_file.write(f"Schema for Table: {file_name}\n\n")
    table_content+=f"Schema for Table: {file_name}\n\n"


    # Get the Heading
    h1_element = soup.find('h1')
    table_content+=f"{h1_element.text.strip()}\n\n"


    # Get the Schema
    next_tag = h1_element.find_next()

    # Print the text <p> content
    if next_tag:
        table_content+="About Table :" + f"{next_tag.text.strip()}\n\n"
    else:
        print("No <p> tag found after the <h1> tag.")

    # Get Text of ID
    id_element = soup.find(id="table-usage-guide")
    next_tag = id_element.find_next()
    # print("Table Usage Guide: ",next_tag.text.strip())

    table_content+="Table Usage Guide: " + f"{next_tag.text.strip()}\n\n"


    table_content_alpha = scrap_steampipe(url,response)
    table_content+=table_content_alpha

    # Get the Schema
    schema_element = soup.find(id="inspect")
    next_tag = schema_element.find_next()
    # print(f"{schema_element.text.strip()}: ")
    table_content+=f"{schema_element.text.strip()}: \n\n"
    
    # Get the Table
    table_element = soup.find('table', class_='mt-4 table')
    if table_element:
        # Find the <thead> and <tbody> elements within the table
        thead = table_element.find('thead')
        tbody = table_element.find('tbody')

        # Print the text content of <thead>
        if thead:
            for x in thead.find_all('th'):
                table_content += x.text.strip() + "\t"
        else:
            print("No <thead> found in the table.")

        table_content+="\n"
        # Print the text content of <tbody>
        if tbody:
            for x in tbody.find_all('tr'):
                for y in x.find_all('td'):
                    table_content += y.text.strip() + "\t"
                table_content+="\n"
        else:
            print("No <tbody> found in the table.")
    else:
        print("No table with class 'mt-4 table' found.")

    data_file.write(table_content)
    print(f"{file_name} Prompt Size: ", len(table_content)) 

    


# Example usage
urls = [
    "https://hub.steampipe.io/plugins/turbot/aws/tables/aws_ec2_instance",
    "https://hub.steampipe.io/plugins/turbot/aws/tables/aws_ec2_instance_metric_cpu_utilization",
    "https://hub.steampipe.io/plugins/turbot/aws/tables/aws_ec2_instance_metric_cpu_utilization_daily",
    "https://hub.steampipe.io/plugins/turbot/aws/tables/aws_ec2_instance_metric_cpu_utilization_hourly",
    "https://hub.steampipe.io/plugins/turbot/aws/tables/aws_ec2_launch_configuration",


]

for x in urls:
    response = requests.get(x)
    scrap_schema_for_table(x,response)
url_to_scrape = 'https://hub.steampipe.io/plugins/turbot/aws/tables/aws_ec2_instance'
# response = requests.get(url_to_scrape)
# # scrap_steampipe(url_to_scrape, response)
# scrap_schema_for_table(url_to_scrape,response)
