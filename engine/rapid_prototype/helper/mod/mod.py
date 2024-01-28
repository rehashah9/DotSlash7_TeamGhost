import os
import subprocess
class Thrifty:
    def __init__(self):
        pass

    def aws_check_benchmark(self, query):
        ## Run SteamPipe Cli Command
        try:
            if query == "ec2":
                command = ["sudo" , "./aws/steampipe-mod-aws-thrifty" , "steampipe", "check", f"benchmark.{query}", "--output", "json"]

                # Run the subprocess with stdout and stderr redirected to subprocess.PIPE
                process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                output = process.stdout

                # Check the return code
                return_code = process.returncode

                # If the return code is not 0, raise an exception
                if return_code != 0:

                    raise Exception(f"Command {command} returned code {return_code}")

                
                return output

        except Exception as e:
            print("Error at AWS Check Benchmark: ", e)
            print(e)
            return "Error"



alpha = Thrifty()

print(alpha.aws_check_benchmark("ec2"))