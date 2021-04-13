from stac_validator import stac_validator


def main():
    stac_file = "/https://radarstac.s3.amazonaws.com/stac/catalog.json"
    stac = stac_validator.StacValidate(stac_file)
    stac.run()
    print(stac.message)


if __name__ == "__main__":
    main()
