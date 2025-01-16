import pytest

import xe_a207

# Taxable tests
## Taxable.__init__() tests
@pytest.mark.parametrize("vat1, vat2, vat3, vat4", [(vat1, vat2, vat3, vat4) for vat1 in [False, True] for vat2 in [False, True] for vat3 in [False, True] for vat4 in [False, True]])
def test_taxable_init_valid(vat1, vat2, vat3, vat4):
    xe_a207.Taxable(vat1, vat2, vat3, vat4)

@pytest.mark.parametrize("vat2, vat3, vat4", [(vat2, vat3, vat4) for vat2 in [False, True] for vat3 in [False, True] for vat4 in [False, True]])
def test_taxable_init_vat1_invalid(invalid_subject_to_VAT, vat2, vat3, vat4):
    with pytest.raises(AssertionError):
        xe_a207.Taxable(invalid_subject_to_VAT, vat2, vat3, vat4)

@pytest.mark.parametrize("vat1, vat3, vat4", [(vat1, vat3, vat4) for vat1 in [False, True] for vat3 in [False, True] for vat4 in [False, True]])
def test_taxable_init_vat2_invalid(vat1, invalid_subject_to_VAT, vat3, vat4):
    with pytest.raises(AssertionError):
        xe_a207.Taxable(vat1, invalid_subject_to_VAT, vat3, vat4)

@pytest.mark.parametrize("vat1, vat2, vat4", [(vat1, vat2, vat4) for vat1 in [False, True] for vat2 in [False, True] for vat4 in [False, True]])
def test_taxable_init_vat3_invalid(vat1, vat2, invalid_subject_to_VAT, vat4):
    with pytest.raises(AssertionError):
        xe_a207.Taxable(vat1, vat2, invalid_subject_to_VAT, vat4)

@pytest.mark.parametrize("vat1, vat2, vat3", [(vat1, vat2, vat3) for vat1 in [False, True] for vat2 in [False, True] for vat3 in [False, True]])
def test_taxable_init_vat4_invalid(vat1, vat2, vat3, invalid_subject_to_VAT):
    with pytest.raises(AssertionError):
        xe_a207.Taxable(vat1, vat2, vat3, invalid_subject_to_VAT)

## Taxable equality tests
def test_taxable_equal(taxable_equal):
    assert taxable_equal == taxable_equal

def test_taxable_inequal(taxable_inequal):
    assert taxable_inequal[0] != taxable_inequal[1]

## Taxable.from_byte tests
def test_taxable_from_byte_valid(taxable_valid_byte):
    assert taxable_valid_byte[1] == xe_a207.Taxable.from_byte(taxable_valid_byte[0])

def test_taxable_from_byte_invalid(taxable_invalid_byte):
    with pytest.raises(AssertionError):
        xe_a207.Taxable.from_byte(taxable_invalid_byte)

## Taxable.to_byte tests
def test_taxable_to_byte(taxable_valid_byte):
    assert taxable_valid_byte[0] == taxable_valid_byte[1].to_byte()

# Department tests
def test_department_init_valid(dept_valid_code, valid_sales_type, valid_open, valid_preset, valid_taxable, valid_halo, valid_group_no, valid_price, valid_text):
    xe_a207.Department(dept_valid_code, valid_sales_type, valid_open, valid_preset, valid_taxable, valid_halo, valid_group_no, valid_price, valid_text)

def test_department_init_invalid(dept_invalid_code, invalid_sales_type, invalid_open, invalid_preset, invalid_taxable, invalid_halo, invalid_group_no, invalid_price, invalid_text):
    with pytest.raises(AssertionError):
        xe_a207.Department(dept_invalid_code, invalid_sales_type, invalid_open, invalid_preset, invalid_taxable, invalid_halo, invalid_group_no, invalid_price, invalid_text)

def test_department_from_bytes_valid(dept_valid_bytes):
    dept = dept_valid_bytes[1]
    dept_from_bytes = xe_a207.Department.from_bytes(dept_valid_bytes[0])
    assert dept == dept_from_bytes

def test_department_from_bytes_invalid(dept_invalid_bytes):
    with pytest.raises(Exception):
        xe_a207.Department.from_bytes(dept_invalid_bytes)

def test_department_to_bytes_valid(dept_valid_bytes):
    dept_to_bytes = dept_valid_bytes[1].to_bytes()
    dept_in_bytes = dept_valid_bytes[0]
    assert dept_to_bytes == dept_in_bytes

# TODO Department methods tests

# Product tests
def test_product_init_valid(prod_valid_code, prod_valid_dept_no, valid_open, valid_preset, valid_price, valid_text):
    xe_a207.Product(prod_valid_code, prod_valid_dept_no, valid_open, valid_preset, valid_price, valid_text)

def test_product_init_invalid(prod_invalid_code, prod_invalid_dept_no, invalid_open, invalid_preset, invalid_price, invalid_text):
    with pytest.raises(AssertionError):
        xe_a207.Product(prod_invalid_code, prod_invalid_dept_no, invalid_open, invalid_preset, invalid_price, invalid_text)

# TODO Product methods tests

# Logo tests
# TODO all Logo tests, for which more information on how the cash register receives, saves and sends the logo itself
# TODO Kind of Logo file to be loaded into original PC-Link is clear (BMP 130 (H) x 360 (W) Pixel, less than 35% "Schwarzbereich" vom Gesamtbereich)

# Logo message tests
def test_logo_msg_init_valid(valid_logo_msg):
    xe_a207.Logo_msg(valid_logo_msg)

def test_logo_msg_init_invalid(invalid_logo_msg):
    with pytest.raises(AssertionError):
        xe_a207.Logo_msg(invalid_logo_msg)

# TODO Logo message methods tests