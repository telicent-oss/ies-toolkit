import re

RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
XSD = "http://www.w3.org/2001/XMLSchema#"
IES_TOP = "http://purl.org/ies/top/v0/ont/"
IES_CORE = "http://purl.org/ies/core/v0/ont/"
ISO_8601 = "http://iso8601.iso.org/"
ICAL = "http://www.w3.org/2002/12/cal/ical#"  # W3C RDF Calendar vocab (iCalendar / RFC 5545)

RDF_TYPE = f"{RDF}type"

RDFS_CLASS = f"{RDFS}Class"
RDFS_COMMENT = f"{RDFS}comment"
RDFS_LABEL = f"{RDFS}label"
RDFS_RESOURCE = f"{RDFS}Resource"
RDFS_SUBCLASSOF = f"{RDFS}subClassOf"
RDFS_SUBPROPERTYOF = f"{RDFS}subPropertyOf"


# XSD String Types
XSD_STRING = f"{XSD}string"
XSD_NORMALIZED_STRING = f"{XSD}normalizedString"
XSD_TOKEN = f"{XSD}token"
XSD_LANGUAGE = f"{XSD}language"
XSD_NAME = f"{XSD}Name"
XSD_NCNAME = f"{XSD}NCName"

# XSD Numeric Types
XSD_DECIMAL = f"{XSD}decimal"
XSD_INTEGER = f"{XSD}integer"
XSD_LONG = f"{XSD}long"
XSD_INT = f"{XSD}int"
XSD_SHORT = f"{XSD}short"
XSD_BYTE = f"{XSD}byte"
XSD_NON_NEGATIVE_INTEGER = f"{XSD}nonNegativeInteger"
XSD_POSITIVE_INTEGER = f"{XSD}positiveInteger"
XSD_UNSIGNED_LONG = f"{XSD}unsignedLong"
XSD_UNSIGNED_INT = f"{XSD}unsignedInt"
XSD_UNSIGNED_SHORT = f"{XSD}unsignedShort"
XSD_UNSIGNED_BYTE = f"{XSD}unsignedByte"
XSD_NON_POSITIVE_INTEGER = f"{XSD}nonPositiveInteger"
XSD_NEGATIVE_INTEGER = f"{XSD}negativeInteger"
XSD_FLOAT = f"{XSD}float"
XSD_DOUBLE = f"{XSD}double"

# XSD Date/Time Types
XSD_DATETIME = f"{XSD}dateTime"
XSD_DATE = f"{XSD}date"
XSD_TIME = f"{XSD}time"
XSD_DURATION = f"{XSD}duration"
XSD_YEAR_MONTH = f"{XSD}gYearMonth"
XSD_YEAR = f"{XSD}gYear"
XSD_MONTH_DAY = f"{XSD}gMonthDay"
XSD_DAY = f"{XSD}gDay"
XSD_MONTH = f"{XSD}gMonth"

# XSD Boolean Type
XSD_BOOLEAN = f"{XSD}boolean"

# XSD Binary Types
XSD_HEX_BINARY = f"{XSD}hexBinary"
XSD_BASE64_BINARY = f"{XSD}base64Binary"

# XSD URI Type
XSD_ANY_URI = f"{XSD}anyURI"

# Collection of all valid XSD datatypes for validation
VALID_XSD_DATATYPES = frozenset({
    # String Types
    XSD_STRING,
    XSD_NORMALIZED_STRING,
    XSD_TOKEN,
    XSD_LANGUAGE,
    XSD_NAME,
    XSD_NCNAME,
    # Numeric Types
    XSD_DECIMAL,
    XSD_INTEGER,
    XSD_LONG,
    XSD_INT,
    XSD_SHORT,
    XSD_BYTE,
    XSD_NON_NEGATIVE_INTEGER,
    XSD_POSITIVE_INTEGER,
    XSD_UNSIGNED_LONG,
    XSD_UNSIGNED_INT,
    XSD_UNSIGNED_SHORT,
    XSD_UNSIGNED_BYTE,
    XSD_NON_POSITIVE_INTEGER,
    XSD_NEGATIVE_INTEGER,
    XSD_FLOAT,
    XSD_DOUBLE,
    # Date/Time Types
    XSD_DATETIME,
    XSD_DATE,
    XSD_TIME,
    XSD_DURATION,
    XSD_YEAR_MONTH,
    XSD_YEAR,
    XSD_MONTH_DAY,
    XSD_DAY,
    XSD_MONTH,
    # Boolean Type
    XSD_BOOLEAN,
    # Binary Types
    XSD_HEX_BINARY,
    XSD_BASE64_BINARY,
    # URI Type
    XSD_ANY_URI,
})

# A scheme-prefixed URI/IRI with no whitespace: <scheme>:<non-space chars>.
_URI_RE = re.compile(r"[A-Za-z][A-Za-z0-9+.\-]*:\S+")
# Characters an RDF IRIREF may not contain (N-Triples/Turtle grammar): control
# chars U+0000-U+0020 and < > " { } | ^ ` \.
_IRI_FORBIDDEN = re.compile(r"[\x00-\x20<>\"{}|^`\\]")


def is_uri(value) -> bool:
    """True if value is a scheme-prefixed URI string with no whitespace and no
    IRIREF-forbidden characters."""
    return (isinstance(value, str)
            and _URI_RE.fullmatch(value) is not None
            and _IRI_FORBIDDEN.search(value) is None)


