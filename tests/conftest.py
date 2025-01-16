import pytest
import xe_a207

# department initialization values
## valid
@pytest.fixture
def dept_valid_code_low():
    return 0

@pytest.fixture
def dept_valid_code_middle():
    return 50

@pytest.fixture
def dept_valid_code_high():
    return 99

@pytest.fixture(params=["dept_valid_code_low", "dept_valid_code_middle", "dept_valid_code_high"])
def dept_valid_code(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def sales_type_normal():
    return False

@pytest.fixture
def sales_type_sics():
    return True

@pytest.fixture(params=["sales_type_normal", "sales_type_sics"])
def valid_sales_type(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def open_value():
    return True

@pytest.fixture
def closed_value():
    return False

@pytest.fixture(params=["open_value", "closed_value"])
def valid_open(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def preset_price():
    return True

@pytest.fixture
def not_preset_price():
    return False

@pytest.fixture(params=["preset_price", "not_preset_price"])
def valid_preset(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def taxable_all():
    return xe_a207.Taxable(True, True, True, True)

@pytest.fixture
def taxable_some():
    return xe_a207.Taxable(True, False, True, False)

@pytest.fixture
def taxable_none():
    return xe_a207.Taxable(False, False, False, False)

@pytest.fixture(params=["taxable_all", "taxable_some", "taxable_none"])
def valid_taxable(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def halo_high():
    return 999999.99

@pytest.fixture
def halo_middle():
    return 50000.50

@pytest.fixture
def halo_low():
    return 0.

@pytest.fixture(params=["halo_high", "halo_middle", "halo_low"])
def valid_halo(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def group_no_plus():
    return 5

@pytest.fixture
def group_no_minus():
    return 10

@pytest.fixture
def group_no_plus_extra():
    return 11

@pytest.fixture
def group_no_minus_extra():
    return 12

@pytest.fixture(params=["group_no_plus", "group_no_minus", "group_no_plus_extra", "group_no_minus_extra"])
def valid_group_no(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def price_low():
    return 0.

@pytest.fixture
def price_middle():
    return 5000.

@pytest.fixture
def price_high():
    return (1e8 - 1 ) / 100.

@pytest.fixture(params=["price_low", "price_middle", "price_high"])
def valid_price(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def text_short():
    return ""

@pytest.fixture
def text_middle():
    return "Test Group"

@pytest.fixture
def text_long():
    return "0000000000000000"

@pytest.fixture(params=["text_short", "text_middle", "text_long"])
def valid_text(request):
    return request.getfixturevalue(request.param)

## invalid
@pytest.fixture
def dept_invalid_code_low():
    return -1

@pytest.fixture
def dept_invalid_code_high():
    return 100

@pytest.fixture
def dept_code_wrong_type():
    return "Wrong Type"

@pytest.fixture(params=["dept_invalid_code_low", "dept_invalid_code_high", "dept_code_wrong_type"])
def dept_invalid_code(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def sales_type_wrong_type():
    return []

@pytest.fixture(params=["sales_type_wrong_type"])
def invalid_sales_type(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def open_wrong_type():
    return float(1)

@pytest.fixture(params=["open_wrong_type"])
def invalid_open(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def preset_wrong_type():
    return dict()

@pytest.fixture(params=["preset_wrong_type"])
def invalid_preset(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def taxable_wrong_type():
    return set()

@pytest.fixture(params=["taxable_wrong_type"])
def invalid_taxable(request):
    return request.getfixturevalue(request.param)


@pytest.fixture
def invalid_halo_low():
    return -0.001

@pytest.fixture
def invalid_halo_high():
    return (1e8-1)/100 + 0.001

@pytest.fixture
def halo_wrong_type():
    return bytes([])

@pytest.fixture(params=["invalid_halo_low", "invalid_halo_high", "halo_wrong_type"])
def invalid_halo(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def invalid_group_no_wrong_low():
    return 0

@pytest.fixture
def invalid_group_no_wrong_high():
    return 13

@pytest.fixture
def invalid_group_no_wrong_type():
    return bytearray()

@pytest.fixture(params=["invalid_halo_low", "invalid_halo_high", "halo_wrong_type"])
def invalid_group_no(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def invalid_price_low():
    return -0.001

@pytest.fixture
def invalid_price_high():
    return (1e8-1)/100 + 0.001

@pytest.fixture
def price_wrong_type():
    return b'101101'

@pytest.fixture(params=["invalid_price_low", "invalid_price_high", "price_wrong_type"])
def invalid_price(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def text_to_long():
    return "123456789abcdefgh"

@pytest.fixture
def text_wrong_type():
    return float(1e50)

@pytest.fixture(params=["text_to_long", "text_wrong_type"])
def invalid_text(request):
    return request.getfixturevalue(request.param)

# product initialization values
## valid
@pytest.fixture
def prod_valid_code_low():
    return 1

@pytest.fixture
def prod_valid_code_middle():
    return 50000

@pytest.fixture
def prod_valid_code_high():
    return 99999

@pytest.fixture(params=["prod_valid_code_low", "prod_valid_code_middle", "prod_valid_code_high"])
def prod_valid_code(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def prod_valid_dept_no_low():
    return 1

@pytest.fixture
def prod_valid_dept_no_middle():
    return 50

@pytest.fixture
def prod_valid_dept_no_high():
    return 99

@pytest.fixture(params=["prod_valid_dept_no_low", "prod_valid_dept_no_middle", "prod_valid_dept_no_high"])
def prod_valid_dept_no(request):
    return request.getfixturevalue(request.param)

## invalid
@pytest.fixture
def prod_invalid_code_low():
    return 0

@pytest.fixture
def prod_invalid_code_high():
    return 100000

@pytest.fixture
def prod_invalid_code_wrong_type():
    return 5.

@pytest.fixture(params=["prod_invalid_code_low", "prod_invalid_code_high", "prod_invalid_code_wrong_type"])
def prod_invalid_code(request):
    return request.getfixturevalue(request.param)

@pytest.fixture
def prod_invalid_dept_no_low():
    return 0

@pytest.fixture
def prod_invalid_dept_no_high():
    return 100

@pytest.fixture
def prod_invalid_dept_no_wrong_type():
    return 50.0

@pytest.fixture(params=["prod_invalid_dept_no_low", "prod_invalid_dept_no_high", "prod_invalid_dept_no_wrong_type"])
def prod_invalid_dept_no(request):
    return request.getfixturevalue(request.param)

# Taxable initialization values
## valid
@pytest.fixture
def subject_to_VAT():
    return True

@pytest.fixture
def not_subject_to_VAT():
    return False

@pytest.fixture(params=["subject_to_VAT", "not_subject_to_VAT"])
def valid_subject_to_VAT_options(request):
    return request.getfixturevalue(request.param)

## invalid
@pytest.fixture
def invalid_subject_to_VAT_wrong_type():
    return "TEST"

@pytest.fixture(params=["invalid_subject_to_VAT_wrong_type"])
def invalid_subject_to_VAT(request):
    return request.getfixturevalue(request.param)

# Logo initialization values
## valid
# TODO have to find out how logo works first

## invalid
# TODO have to find out how logo works first

# Logo_msg initialization values
## valid
@pytest.fixture
def empty_logo_msg_init():
    return []

@pytest.fixture
def single_line_logo_msg_init():
    return ["test_LINE"]

@pytest.fixture
def some_lines_logo_msg_init():
    return ["BLa Bla", "Blubb BluBB"]

@pytest.fixture
def full_lines_logo_msg_init():
    return ["BLa BlaBLa BlaBLa BlaBLa\tBlabd",
            "Blubb BluBBTESTBlubb BluBBBlub",
            "Blubb\tBluBBTESTBlubb BluBBBlub",
            "Blubb BluBBTESTBlubb\tBluBBBlub",
            "Blubb BluBBTE\tSTBlubbBluBBBlub",
            "Blubb BluBBTE\tSTBlubbBluBBBlub",
           ]

@pytest.fixture(params=["empty_logo_msg_init", "single_line_logo_msg_init", "some_lines_logo_msg_init", "full_lines_logo_msg_init"])
def valid_logo_msg(request):
    return request.getfixturevalue(request.param)

## invalid
@pytest.fixture
def logo_msg_to_many_lines():
    return ["",
            "",
            "",
            "",
            "",
            "",
            ""
           ]

@pytest.fixture
def logo_msg_to_long_line():
    return ["BLa BlaBLa",
            "BLa BlaBLa BlaBLa BlaBLa\tBlabd\t",
            "BLa BlaBLa\t",
            "BLa BlaBLatBlabd\t",
            ]

@pytest.fixture
def logo_msg_contains_line_break():
    return ["BLa BlaBLa",
            "BLa BlaBLa BlaBLa BlaBLa\tBlab\n",
            "BLa BlaBLa\t",
            "BLa BlaBLatBlabd\t",
            ]

@pytest.fixture
def logo_msg_wrong_container_type():
    return {}

@pytest.fixture
def logo_msg_wrong_item_type():
    return ["1", 2, "3"]

@pytest.fixture(params=["logo_msg_to_many_lines", "logo_msg_to_long_line", "logo_msg_contains_line_break", "logo_msg_wrong_container_type", "logo_msg_wrong_item_type"])
def invalid_logo_msg(request):
    return request.getfixturevalue(request.param)

# Tax initialization values
## valid
# TODO

## invalid
# TODO

# Taxable values
taxable_values = [
    xe_a207.Taxable(False, False, False, False),
    xe_a207.Taxable(True,  False, False, False),
    xe_a207.Taxable(False, True,  False, False),
    xe_a207.Taxable(True,  True,  False, False),
    xe_a207.Taxable(False, False, True,  False),
    xe_a207.Taxable(True,  False, True,  False),
    xe_a207.Taxable(False, True,  True,  False),
    xe_a207.Taxable(True,  True,  True,  False),
    xe_a207.Taxable(False, False, False, True),
    xe_a207.Taxable(True,  False, False, True),
    xe_a207.Taxable(False, True,  False, True),
    xe_a207.Taxable(True,  True,  False, True),
    xe_a207.Taxable(False, False, True,  True),
    xe_a207.Taxable(True,  False, True,  True),
    xe_a207.Taxable(False, True,  True,  True),
    xe_a207.Taxable(True,  True,  True,  True)
]

# Taxable byte conversion test values
## valid
@pytest.fixture(params=zip(range(16), taxable_values))
def taxable_valid_byte(request):
    return request.param

## invalid
@pytest.fixture
def taxable_invalid_low():
    return -1

@pytest.fixture
def taxable_invalid_high():
    return 16

@pytest.fixture
def taxable_invalid_wrong_type():
    return "test"

@pytest.fixture(params=["taxable_invalid_low", "taxable_invalid_high", "taxable_invalid_wrong_type"])
def taxable_invalid_byte(request):
    return request.getfixturevalue(request.param)

# Taxable equality test data
@pytest.fixture(params=taxable_values)
def taxable_equal(request):
    return request.param

# Taxable inequality test data
@pytest.fixture(params=[(taxable_values[i], taxable_values[j]) for i in range(len(taxable_values)) for j in range(len(taxable_values)) if i != j])
def taxable_inequal(request):
    return request.param

# Department byte conversion test data
## valid
@pytest.fixture
def dept_open_preset_normsales_no_tax(request):
    code = 1
    sales_type = request.getfixturevalue("sales_type_normal")
    open_ = request.getfixturevalue("open_value")
    preset = request.getfixturevalue("preset_price")
    taxable = request.getfixturevalue("taxable_none")
    halo = 2.
    price = 0.5
    group_no = request.getfixturevalue("group_no_plus")
    text = "Heißgetränke"
    return (bytes([
        1,3,0,0,0,2,0,5,0,0,0,80,72,101,105,225,103,101,116,114,132,110,107,101,0,0, 0, 0
        ]),
        xe_a207.Department(code, sales_type, open_, preset, taxable, halo, group_no, price, text))

@pytest.fixture
def dept_open_notpreset_normsales_some_tax(request):
    code = 14
    sales_type = request.getfixturevalue("sales_type_normal")
    open_ = request.getfixturevalue("open_value")
    preset = request.getfixturevalue("not_preset_price")
    taxable = request.getfixturevalue("taxable_some")
    halo = request.getfixturevalue("halo_middle")
    price = request.getfixturevalue("price_high")
    group_no = request.getfixturevalue("group_no_plus_extra")
    text = "Auszahlung"
    return (bytes([0x14, 0x01, 0b0101, 0x05, 0x00, 0x00, 0x50, 0x11, 0x99, 0x99, 0x99, 0x99, 65, 117, 115, 122, 97, 104, 108, 117, 110, 103, 0, 0, 0, 0, 0, 0]),
            xe_a207.Department(code, sales_type, open_, preset, taxable, halo, group_no, price, text))

@pytest.fixture(params=["dept_open_preset_normsales_no_tax", "dept_open_notpreset_normsales_some_tax"])
def dept_valid_bytes(request):
    return request.getfixturevalue(request.param)

## invalid
@pytest.fixture
def dept_invalid_code():
    return bytes([
        #code | sales preset open | VAT |    HALO           | group no |        price       | text
        0xFF,   0x03,               0x00,0x00,0x00,0x02,0x00,   0x01,   0x00,0x00,0x00,0x50 ,80,72,101,105,225,103,101,116,114,132,110,107,101,0, 0, 0
    ])

@pytest.fixture
def dept_invalid_sales_open_preset_byte():
    return bytes([
        #code | sales preset open | VAT |    HALO           | group no |        price       | text
        0x01,   0xFF,               0x00,0x00,0x00,0x02,0x00,   0x01,   0x00,0x00,0x00,0x50 ,80,72,101,105,225,103,101,116,114,132,110,107,101,0, 0, 0
    ])

@pytest.fixture
def dept_invalid_vat():
    return bytes([
        #code | sales preset open | VAT |    HALO           | group no |        price       | text
        0x01,   0x03,               0xFF,0x00,0x00,0x02,0x00,   0x01,   0x00,0x00,0x00,0x50 ,80,72,101,105,225,103,101,116,114,132,110,107,101,0, 0, 0
    ])

@pytest.fixture
def dept_invalid_halo():
    return bytes([
        #code | sales preset open | VAT |    HALO           | group no |        price       | text
        0x01,   0x03,               0x00,0xFF,0xFF,0x02,0x00,   0x01,   0x00,0x00,0x00,0x50 ,80,72,101,105,225,103,101,116,114,132,110,107,101,0, 0, 0
    ])

@pytest.fixture
def dept_invalid_group_no():
    return bytes([
        #code | sales preset open | VAT |    HALO           | group no |        price       | text
        0x01,   0x03,               0x00,0x00,0x00,0x02,0x00,   0x0A,   0x00,0x00,0x00,0x50 ,80,72,101,105,225,103,101,116,114,132,110,107,101,0, 0, 0
    ])

@pytest.fixture
def dept_invalid_price():
    return bytes([
        #code | sales preset open | VAT |    HALO           | group no |        price       | text
        0x01,   0x03,               0x00,0x00,0x00,0x02,0x00,   0x01,   0x00,0x00,0x00,0xA0 ,80,72,101,105,225,103,101,116,114,132,110,107,101,0, 0, 0
    ])

@pytest.fixture
def dept_invalid_length():
    return bytes([
        #code | sales preset open | VAT |    HALO           | group no |        price       | text
        0x01,   0x03,               0x00,0x00,0x00,0x02,0x00,   0x01,   0x00,0x00,0x00,0x50 ,80,72,101,105,225,103,101,116,114,132,110,107,101,0, 0, 0, 0
    ])

@pytest.fixture(params=["dept_invalid_code", "dept_invalid_sales_open_preset_byte", "dept_invalid_vat", "dept_invalid_halo", "dept_invalid_group_no", "dept_invalid_price", "dept_invalid_length"])
def dept_invalid_bytes(request):
    return request.getfixturevalue(request.param)