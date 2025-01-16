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
        """initializes new Department object

        Args:
            code (int):         Number/Code of the Department
            sales_type (bool):  Normal sales type (True), SICS (False)
            open (bool):        price can be changed (True) or not (False)
            preset (bool):      is preset default price (True) or not (False)
            taxable (Taxable):  valid Taxable
            halo (float):       highest allowed price
            group_no (int):     group number (1-9 => plus department, 10 => minus department, 11 => plus extra department, 12 => minus extra department)
            price (float):      default price of the department
            text (str):         department name
        """
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
        assert isinstance(group_no, int) and 0 <= group_no <= 12
        self.__group_no = group_no
        assert isinstance(price, float) and 0. <= price <= 999999.99
        self.__price = price
        assert isinstance(text, str) and len(text) <= 16
        self.__text = text

    def from_bytes(B: bytes):
        """creates a new department object from bytes
        Format:
            B[0] - code
            B[1] - infos for single item cash sales, preset price and open price
                    b'000S00PO'
                    S is 1 if single item cash sales, P is 1 if preset default price is used, O is 1 if price is open for change
            B[2] - VATs that should be applied
                    b'0000ABCD'
                    A is 1 if VAT1, B is 1 if VAT2, C is 1 if VAT3 and D is 1 if VAT4 applies (multiple VATs are possible to apply)
            B[3:7] - halo (highest amount lockout) aka highest price that can be used with this department
                    hex format (but only decimal numbers are used!)
            B[7] - Group number
                    1-9 Plus department
                    10 Minus department
                    11 Plus extra department
                    12 Minus extra department
                    hex format (but only decimal numbers are used!)
            B[8:12] - default price for this department (only used if preset is set)
                    hex format (but only decimal numbers are used!)
            B[12:28] - department name decoded with DOS Latin US (Code page 437)
            all other Bytes/Bits are zeros

        Args:
            B (bytes): bytes of a single department
        Returns:
            Department: a new Department object with the data from the given bytes
        """
        assert len(B) == 28
        preset_open_sale_type = int(B[1])
        _code = int(B[0:1].hex())
        assert (preset_open_sale_type & (~0b10011)) == 0
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
        """Converts the department into bytes of the format:
            B[0] - code
            B[1] - infos for single item cash sales, preset price and open price
                    b'000S00PO'
                    S is 1 if single item cash sales, P is 1 if preset default price is used, O is 1 if price is open for change
            B[2] - VATs that should be applied
                    b'0000DCBA'
                    A is 1 if VAT1, B is 1 if VAT2, C is 1 if VAT3 and D is 1 if VAT4 applies (multiple VATs are possible to apply)
            B[3:7] - halo (highest amount lockout) aka highest price that can be used with this department
                    hex format (but only decimal numbers are used!)
            B[7] - Group number
                    1-9 Plus department
                    10 Minus department
                    11 Plus extra department
                    12 Minus extra department
                    hex format (but only decimal numbers are used!)
            B[8:12] - default price for this department (only used if preset is set)
                    hex format (but only decimal numbers are used!)
            B[12:28] - department name decoded with DOS Lating US (Code page 437)
            all other Bytes/Bits are zeros

        Returns:
            bytes: Bytes that can be read by the cash register
        """
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
    
    def __eq__(self, other):
        return (
            self.__code == other.__code and
            self.__open == other.__open and
            self.__preset == other.__preset and
            self.__sales_type == other.__sales_type and
            self.__group_no == other.__group_no and
            int(self.__price * 100.) == int(other.__price * 100.) and
            int(self.__halo * 100.) == int(other.__halo * 100.) and
            self.__text == other.__text)

    def __ne__(self, other):
        return (
            self.__code != other.__code or
            self.__open != other.__open or
            self.__preset != other.__preset or
            self.__sales_type != other.__sales_type or
            self.__group_no != other.__group_no or
            int(self.__price * 100.) != int(other.__price * 100.) or
            int(self.__halo * 100.) != int(other.__halo * 100.) or
            self.__text != other.__text
        )

    def __hash__(self):
        return int(self.to_bytes().hex(), 16)

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

    def __eq__(self, other):
        return (
            self.__code == other.__code and
            self.__dept_no == other.__dept_no and
            self.__open == other.__open and
            self.__preset == other.__preset and
            int(self.__price * 100.) == int(other.__price * 100.) and
            self.__text == other.__text)

    def __ne__(self, other):
        return (
            self.__code != other.__code or
            self.__dept_no != other.__dept_no or
            self.__open != other.__open or
            self.__preset != other.__preset or
            int(self.__price * 100.) != int(other.__price * 100.) or
            self.__text != other.__text)

    def __hash__(self):
        return int(self.to_bytes().hex(), 16)

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
        assert isinstance(byte, int)
        assert 0 <= byte < 16
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

    def __eq__(self, other):
        if (isinstance(other, self.__class__) and
            self.__tax_1 == other.__tax_1 and
            self.__tax_2 == other.__tax_2 and
            self.__tax_3 == other.__tax_3 and
            self.__tax_4 == other.__tax_4):
            return True
        return False
    
    def __ne__(self, other):
        if (not isinstance(other, self.__class__) or
            self.__tax_1 != other.__tax_1 or
            self.__tax_2 != other.__tax_2 or
            self.__tax_3 != other.__tax_3 or
            self.__tax_4 != other.__tax_4):
            return True
        return False
    
    def __hash__(self):
        return self.to_byte()

# TODO
class Logo:
    pass

class Logo_msg:
    __rows: list[str]
    
    def __init__(self, rows: list[str]):
        self.__rows = []
        assert isinstance(rows, list)
        assert len(rows) <= 6
        for row in rows:
            assert isinstance(row, str)
            assert len(row) <= 30
            assert "\n" not in row
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

class Programming:
    dept: list[Department]
    plu: list[Product]
    logo: Logo
    logo_msg: Logo_msg
    tax: list[Tax]
    
    def __init__(self, 
        dept: list[Department],
        plu: list[Product],
        logo: Logo,
        logo_msg: Logo_msg,
        tax: list[Tax]):
        assert isinstance(dept, list) and all(map(lambda x: isinstance(x, Department), dept))
        self.dept = dept
        assert isinstance(plu, list) and all(map(lambda x: isinstance(x, Product), plu))
        self.plu = plu
        assert isinstance(logo, Logo)
        self.logo = logo
        assert isinstance(logo_msg, Logo_msg)
        self.logo_msg = logo_msg
        assert isinstance(tax, list) and all(map(lambda x: isinstance(x, Tax), tax))
        self.tax = tax

    def read_directory(directory: str):
        products_file = directory + "/PROGRAM/PLUDT.SDA"
        departments_file = directory + "/PROGRAM/DEPTDT.SDA"
        taxes_file = directory + "/PROGRAM/TAXTB.SDA"
        logo_msg_file = directory + "/PROGRAM/LOGODT.SDA"
        
        dept = import_departments(departments_file)
        plu = import_products(products_file)
        #logo = import_logo(logo_file)
        logo_msg = import_logo_msg(logo_msg_file)
        tax = import_taxes(taxes_file)

    def write_directory(self, directory: str):
        products_file = directory + "/PROGRAM/PLUDT.SDA"
        departments_file = directory + "/PROGRAM/DEPTDT.SDA"
        taxes_file = directory + "/PROGRAM/TAXTB.SDA"
        logo_msg_file = directory + "/PROGRAM/LOGODT.SDA"
        return (export_products(products_file, self.products),
                export_departments(departments_file, self.departments),
                export_taxes(taxes_file, self.taxes),
                export_logo_msg(logo_msg_file, self.logo_msg))

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
