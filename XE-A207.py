"""Module for the SD Card Programming of a SHARP XE-A207 cash register
"""
class Department:
    """Department used in an SHARP XE-A207 cash register as displayed in the according PC-LINK program"""
    __code: int
    __text: str
    __price: float
    __open: bool
    __preset: bool
    __sales_type: bool
    __halo: float
    __group_no: int

    def __init__(self,
                 code: int,
                 sales_type: bool,
                 open: bool,
                 preset: bool,
                 taxable,
                 halo: float,
                 group_no: int,
                 price: float,
                 text: str,
                ):
        assert isinstance(code, int) and code < 100
        self.__code = code
        assert isinstance(sales_type, bool)
        self.__sales_type = sales_type
        assert isinstance(open, bool)
        self.__open = open
        assert isinstance(preset, bool)
        self.__preset = preset
        assert isinstance(taxable, Taxable)
        self.__taxable = taxable
        assert isinstance(halo, float) and 0. <= halo <= 999999.99
        self.__halo = halo
        assert isinstance(group_no, int) and group_no <= 12
        self.__group_no = group_no
        assert isinstance(price, float) and 0. <= price < 1e9
        self.__price = price
        assert isinstance(text, str) and len(text) <= 16
        self.__text = text

    def from_bytes(B: bytes):
        preset_open_sale_type = int(B[1])
        _code = int(B[0:1].hex())
        _sales_type = (preset_open_sale_type & 0b10000) != 0
        _open       = (preset_open_sale_type & 0b00001) != 0
        _preset     = (preset_open_sale_type & 0b00010) != 0
        _taxable    = Taxable.from_byte(B[2])
        _halo       = float(B[3:7].hex())/100.
        _group_no   = int(B[7:8].hex())
        _price      = float(B[8:12].hex())/100.
        _text       = decode_text_part(B[12:28])
        return Department(_code, _sales_type, _open, _preset, _taxable, _halo, _group_no, _price, _text)

    def to_bytes(self) -> bytes:
        B = bytearray([0] * 28)
        B[0:1] = int2hex(self.__code, 1)
        if self.__sales_type:
            B[1] |= 0b10000
        if self.__open:
            B[1] |= 0b00001
        if self.__preset:
            B[1] |= 0b00010
        B[2] = self.__taxable.to_byte()
        B[3:7] = int2hex(int(self.__halo * 100.), 4)
        B[7:8] = int2hex(self.__group_no, 1)
        B[8:12] = int2hex(int(self.__price * 100.), 4)
        B[12:28] = encode_text_part(self.__text, 16)
        return bytes(B)

    def __repr__(self):
        return f"Department(code=({self.__code}), sales_type=({self.__sales_type}), open=({self.__open}), preset=({self.__preset}), taxable=({self.__taxable}), halo=({self.__halo}), group_no=({self.__group_no}), price=({self.__price}), text=({self.__text}))"
        
    def __str__(self):
        return f"{self.__code}\t{self.__sales_type}\t{self.__open}\t{self.__preset}\t{self.__taxable}\t{self.__halo}\t{self.__group_no}\t{self.__price}\t{self.__text}"

class Product:
    __code: int
    __text: str
    __price: float
    __dept_no: int
    __open: bool
    __preset: bool
    def __init__(self,
                 code: int,
                 dept_no: int,
                 open: bool,
                 preset: bool,
                 price: float,
                 text: str
                ):
        assert isinstance(code, int) and 0 < code < 1e6
        self.__code = code
        assert isinstance(dept_no, int) and 1 <= dept_no <= 99
        self.__dept_no = dept_no
        assert isinstance(open, bool)
        self.__open = open
        assert isinstance(preset, bool)
        self.__preset = preset
        assert isinstance(price, float) and 0 <= price < 1e9
        self.__price = price
        assert isinstance(text, str) and len(text) <= 16
        self.__text = text

    def from_bytes(B):
        _code = int(B[5:8].hex())
        _dept_no = int(bytes([B[8]]).hex())
        preset_open_code = int(B[9])
        _open = preset_open_code & 0b01 != 0
        _preset = preset_open_code & 0b10 != 0
        _price = float(B[10:15].hex())/100.
        _text = decode_text_part(B[15:31])
        return Product(_code, _dept_no, _open, _preset, _price, _text)

    def to_bytes(self) -> bytes:
        B = bytearray([0] * 31)
        B[5:8] = int2hex(self.__code, 3)
        B[8:9] = int2hex(self.__dept_no, 1)
        if self.__open:
            B[9] |= 0b01
        if self.__preset:
            B[9] |= 0b10
        B[10:15] = int2hex(int(self.__price * 100.), 5)
        B[15:31] = encode_text_part(self.__text, 16)
        return bytes(B)

    def __repr__(self):
        return f"Product(code={self.__code}, dept_no={self.__dept_no}, open={self.__open}, preset={self.__preset}, price={self.__price}, text={self.__text})"

    def __str__(self):
        return f"{self.__code}\t{self.__dept_no}\t{self.__open}\t{self.__preset}\t{self.__price}\t{self.__text}"

class Taxable:
    __tax_1: bool
    __tax_2: bool
    __tax_3: bool
    __tax_4: bool
    def __init__(self, tax_1: bool, tax_2: bool, tax_3: bool, tax_4: bool):
        assert isinstance(tax_1, bool) 
        self.__tax_1 = tax_1
        assert isinstance(tax_2, bool)
        self.__tax_2 = tax_2
        assert isinstance(tax_3, bool)
        self.__tax_3 = tax_3
        assert isinstance(tax_4, bool)
        self.__tax_4 = tax_4

    def from_byte(byte: int):
        tax_1 = byte & 0b0001 != 0
        tax_2 = byte & 0b0010 != 0
        tax_3 = byte & 0b0100 != 0
        tax_4 = byte & 0b1000 != 0
        return Taxable(tax_1, tax_2, tax_3, tax_4)

    def to_byte(self) -> int:
        B = 0
        if self.__tax_1: B |= 0b0001
        if self.__tax_2: B |= 0b0010
        if self.__tax_3: B |= 0b0100
        if self.__tax_4: B |= 0b1000
        return B

    def __repr__(self):
        return f"Taxable (tax_1 = {self.__tax_1}, tax_2 = {self.__tax_2}, tax_3 = {self.__tax_3}, tax_4 = {self.__tax_4})"

# TODO
class Logo:
    pass

class Logo_msg:
    __rows: list[str]
    
    def __init__(self, rows: list[str]):
        self.__rows = []
        assert len(rows) <= 6
        for row in rows:
            assert len(row) <= 30
            self.__rows.append(row)

    def from_bytes(B: bytes):
        assert len(B) == 186
        rows = []
        for i in range(6):
            rows.append(decode_text_part(B[i*31 + 1:i*31 + 30]))
        return Logo_msg(rows)

    def to_bytes(self) -> bytes:
        assert len(self.__rows) <= 6
        B = bytearray()
        for i in range(len(self.__rows)):
            B = B + bytearray([i+1]) + encode_text_part(self.__rows[i], 30)
        for i in range(len(self.__rows), 6):
            B = B + bytearray([i+1]) + encode_text_part("", 30)
        assert len(B) == 186
        return bytes(B)

    def __repr__(self) -> str:
        repr_ = "Logo_msg(\n"
        for row in self.__rows:
            repr_ = repr_ + "\t'" + row + "'\n"
        repr_ = repr_[:-1] + ")"
        return repr_

    def __str__(self) -> str:
        string = ""
        for row in self.__rows:
            string = string + row + "\n"
        return string

class Tax:
    __number: int
    __tax_rate: float
    __lower_tax_limit: float
    
    def __init__(self, number: int, tax_rate: float, lower_tax_limit: float):
        assert isinstance(number, int) and 0 < number <= 4
        self.__number = number
        assert isinstance(tax_rate, float) and -999.9999 <= tax_rate <= 999.9999
        self.__tax_rate = tax_rate
        assert isinstance(lower_tax_limit, float) and 0 <= lower_tax_limit <= 999.99
        self.__lower_tax_limit = lower_tax_limit

    def __repr__(self):
        return f"Tax(number={self.__number}, tax_rate={self.__tax_rate}, lower_tax_rate={self.__lower_tax_limit})"
    
    def to_bytes(self) -> bytes:
        B = bytearray([0] * 90)
        if (self.__tax_rate == 0 and
            self.__lower_tax_limit == 0):
            return bytes(B)
        B[0] = 1
        if self.__tax_rate < 0.:
            B[1] = b'\x0D'
        B[2:6] = int2hex(int(self.__tax_rate * 1e4), 4)
        B[9:12] = int2hex(int(self.__lower_tax_limit * 100), 3)
        return bytes(B)

def import_programming(directory: str):
    products_file = directory + "/PROGRAM/PLUDT.SDA"
    departments_file = directory + "/PROGRAM/DEPTDT.SDA"
    taxes_file = directory + "/PROGRAM/TAXTB.SDA"
    logo_msg_file = directory + "/PROGRAM/LOGODT.SDA"
    return import_products(products_file), import_departments(departments_file), import_taxes(taxes_file), import_logo_msg(logo_msg_file)

def export_programming(directory: str, products: list[Product], departments: list[Department], taxes: list[Tax], logo_msg: Logo_msg):
    products_file = directory + "/PROGRAM/PLUDT.SDA"
    departments_file = directory + "/PROGRAM/DEPTDT.SDA"
    taxes_file = directory + "/PROGRAM/TAXTB.SDA"
    logo_msg_file = directory + "/PROGRAM/LOGODT.SDA"
    return (export_products(products_file, products),
            export_departments(departments_file, departments),
            export_taxes(taxes_file, taxes),
            export_logo_msg(logo_msg_file, logo_msg))

def import_products(file: str):
    products = []
    with open(file, 'br') as f:
        while (B := f.read(31)):
            products.append(Product.from_bytes(B))
    return products

def export_products(file: str, products: list[Product]):
    with open(file, 'bw') as f:
        B = bytearray([])
        for prod in products:
            assert isinstance(prod, Product)
            prod_bytes = prod.to_bytes()
            assert len(prod_bytes) == 31, f"{len(prod_bytes)}, {prod_bytes}"
            B = B + prod_bytes
        assert len(products) * 31 == len(B)
        return B

def import_departments(file: str):
    departments = []
    with open(file, 'br') as f:
        while (B := f.read(28)):
            departments.append(Department.from_bytes(B))
    return departments

def export_departments(file: str, department: list[Department]):
    with open(file, 'bw') as f:
        B = bytearray([])
        for dept in department:
            assert isinstance(dept, Department)
            dept_bytes = dept.to_bytes()
            assert len(dept_bytes) == 28
            B = B + dept_bytes
        assert len(department) * 28 == len(B)
        f.write(B)
        return B

def import_taxes(file: str):
    taxes = []
    with open(file, 'br') as f:
        i = 1
        while (B := f.read(90)):
            _tax_no = i
            _tax_rate = float(B[2:6].hex()) / 1e4
            if B[1] == 13:
                _tax_rate *= -1
            _lower_tax_limit = float(B[9:12].hex()) / 100
            taxes.append(Tax(_tax_no, _tax_rate, _lower_tax_limit))
    return taxes

def export_taxes(file: str, taxes: list[Tax]):
    with open(file, "bw") as f:
        B = bytearray([])
        for tax in taxes:
            assert isinstance(tax, Tax)
            tax_bytes = tax.to_bytes()
            assert len(tax_bytes) == 90
            B = B + tax_bytes
        assert len(taxes) * 90 == len(B)
        f.write(B)
        return B

def import_logo_msg(file: str) -> Logo_msg:
    logo_msg: Logo_msg
    with open(file, "br") as f:
        logo_msg = Logo_msg.from_bytes(f.read())
    return logo_msg

def export_logo_msg(file: str, logo_msg: Logo_msg):
    with open(file, "bw") as f:
        f.write(logo_msg.to_bytes())

def decode_text_part(B: bytes) -> str:
    string = []
    for character in B:
        if character == 0:
            break
        string.append(character)
    return bytes(string).decode("cp437")

def encode_text_part(string: str, alignment: int) -> bytes:
    assert len(string) <= alignment
    B = bytearray(string.encode("cp437"))
    for _ in range(len(B), alignment):
        B = B + bytearray([0])
    return B

def int2hex(number: int, alignment: int):
    text = str(number)
    if len(text) % 2 != 0:
        text = "0" + text
    for _ in range(len(text) // 2, alignment):
        text = "00" + text
    return bytearray.fromhex(text)
