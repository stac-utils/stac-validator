from stac_validator import stac_validator


def main():
    stac_file = "/https://radarstac.s3.amazonaws.com/stac/catalog.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    print(stac.message)
    output = stac.message[0]
    if "validation method" in output:
        output.pop("validation method")
    print(output)


if __name__ == "__main__":
    main()
