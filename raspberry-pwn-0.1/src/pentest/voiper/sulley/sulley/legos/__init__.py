import ber
import dcerpc
import misc
import xdr
import sip

# all defined legos must be added to this bin.
BIN = {}
BIN["ber_string"]           = ber.string
BIN["ber_integer"]          = ber.integer
BIN["dns_hostname"]         = misc.dns_hostname
BIN["ip_address_ascii"]     = misc.ip_address_ascii
BIN["ndr_conformant_array"] = dcerpc.ndr_conformant_array
BIN["ndr_wstring"]          = dcerpc.ndr_wstring
BIN["ndr_string"]           = dcerpc.ndr_string
BIN["tag"]                  = misc.tag
BIN["xdr_string"]           = xdr.string
BIN["ip_address_ascii"]	= misc.ip_address_ascii
BIN["ipv6_address_ascii"] = misc.ipv6_address_ascii
BIN["static_credentials"] = sip.static_credentials 
BIN["static_challenge"] = sip.static_challenge 
BIN["q_value"] = sip.q_value
BIN["to_sip_uri"] = sip.to_sip_uri
BIN["from_sip_uri"] = sip.from_sip_uri
BIN["to_sip_uri_basic"]	= sip.to_sip_uri_basic
BIN["from_sip_uri_basic"] = sip.from_sip_uri_basic
