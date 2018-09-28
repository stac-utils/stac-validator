"""
Description: Test the validator

"""
__author__ = "James Banting"
import stac_validator
import multiprocessing

manager = multiprocessing.Manager()
lock = multiprocessing.Lock()

def test_good_item_validation_v052():
    verbose_dict = manager.dict()
    summary_dict = manager.dict()
    stac_validator.StacValidate(
        stac_file="tests/test_data/good_item_v052.json",
        verbose_dict=verbose_dict,
        summary_dict=summary_dict,
        lock=lock,
        version="v0.5.2",
        verbose=True
    )
    print(verbose_dict)
    assert verbose_dict.copy() == {
        'tests/test_data/good_item_v052.json': {
            'asset_type': 'item',
            'valid_stac': True
        }
    }


def test_good_catalog_validation_v052():
    verbose_dict = manager.dict()
    summary_dict = manager.dict()
    stac_validator.StacValidate(
        stac_file="tests/test_data/good_catalog_v052.json",
        verbose_dict=verbose_dict,
        summary_dict=summary_dict,
        lock=lock,
        version="v0.5.2",
        verbose=True
    )
    print(verbose_dict)
    assert verbose_dict.copy() == {
        'tests/test_data/good_catalog_v052.json': {
            'asset_type': 'catalog',
            'valid_stac': True
        }
    }

def test_verbose():
    verbose_dict = manager.dict()
    summary_dict = manager.dict()
    stac_validator.StacValidate(
        stac_file="tests/test_data/good_catalog_v052.json",
        verbose_dict=verbose_dict,
        summary_dict=summary_dict,
        lock=lock,
        version="v0.5.2",
        verbose=False
    )
    print(verbose_dict)
    assert verbose_dict.copy() == {}
    print(summary_dict)
    assert summary_dict.copy() == {'catalogs_valid': 1}


def test_nested_catalog():
    verbose_dict = manager.dict()
    summary_dict = manager.dict()
    stac_validator.StacValidate(
        stac_file="tests/test_data/nested_catalogs/parent_catalog.json",
        verbose_dict=verbose_dict,
        summary_dict=summary_dict,
        lock=lock,
        version="v0.5.2",
        verbose=False
    )
    print(summary_dict)
    assert summary_dict.copy() == {
        'catalogs_valid': 3,
        'catalogs_invalid': 1,
        'items_valid': 4,
        'items_invalid': 1
    }


def test_geojson_error():
    # Error comes from different versions
    verbose_dict = manager.dict()
    summary_dict = manager.dict()
    stac_validator.StacValidate(
        stac_file="tests/test_data/nested_catalogs/parent_catalog.json",
        lock=lock,
        summary_dict=summary_dict,
        verbose_dict=verbose_dict,
        version="v0.4.0",
        verbose=False
    )
    print(summary_dict)
    assert summary_dict.copy() == {
        'catalogs_invalid': 4,
        'items_invalid': 5
    }
