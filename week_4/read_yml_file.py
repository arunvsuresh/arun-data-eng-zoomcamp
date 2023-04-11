from timeit import default_timer as timer
import yaml

# start = timer()
with open("vehicle_schemas.yml", mode="rb") as file:
    schemas = yaml.safe_load(file)
# end = timer()

# print('elapsed time: ', end - start)

