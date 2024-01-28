import subprocess
import json
import csv
import os


class AWS_Thrifty:
    def __init__(self) -> None:
        pass

    def aws_check_benchmark(self,query):
        try:
            print(query)
            # Save the current working directory
            current_dir = os.getcwd()

            # Change the working directory to the directory of this script
            script_dir = os.path.dirname(os.path.abspath(__file__))
            os.chdir(script_dir)

            ## Check if query file exists
            # if os.path.isfile(f"{query}.json"):
            #     with open(f"{query}.json") as json_file:
            #         output = json.load(json_file)
            #         print(output)
            #         return output

            command = ["steampipe", "check", f"benchmark.{query}", "--output", "json"]

            # Run the subprocess with stdout and stderr redirected to subprocess.PIPE
            process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            ## Convert Stdout to JSON
            output = process.stdout
            output = json.loads(output)
            print(output)
            ## Save JSON to file
            with open(f"{query}.json", "w") as outfile:
                json.dump(output, outfile)

            return output

        except Exception as e:
            print("Error at AWS Check Benchmark: ", e)
            print(e)
            return "Error"
    


alpha = AWS_Thrifty()
alpha.aws_check_benchmark("ec2")
alpha.aws_check_benchmark("rds")
alpha.aws_check_benchmark("cost_explorer")