#!/usr/bin/env python3

import os
import re
import zipfile


def l1l11l_opy_(keyed_string_literal):
    char_base = 2048
    char_modulus = 7

    string_nr = ord(keyed_string_literal[-1])
    rotated_string_literal = keyed_string_literal[:-1]

    rotation_distance = string_nr % len(rotated_string_literal)
    recoded_string_literal = rotated_string_literal[:rotation_distance] + rotated_string_literal[rotation_distance:]

    return "".join(chr(ord(char) - char_base - (char_index + string_nr) % char_modulus) for char_index, char in enumerate(recoded_string_literal))


def deobfuscate_name(prefix, bits):
    var_names = {
        3: "is_ack",  # not certain
        7: "is_nak",  # not certain
        8: "skip_membership",
        10: "cmd_byte",
        19: "app_id",
        24: "magic_char",  # not certain
        65: "dest",
        82: "logger",
        92: "Python",  # not certain
        114: "message_obj",
        116: "local_pubkey",
        176: "good_patterns",
        179: "error_patterns",
        215: "b64string",
        221: "decrypt_bytes",
        223: "serialize_keypair",
        224: "deserialize_keypair",
        225: "pubkey",
        227: "my_pubkey",
        228: "my_gid",
        229: "serialize_pubkey",
        236: "crypt_bytes",  # not certain
        238: "pubkey_from_compressed",
        239: "message_counter",
        240: "local_keypair",
        242: "shared_secret_bytes",
        246: "bytes_to_crypt",
        247: "deserialize_pubkey",
        248: "sender_gid",
        250: "sender_pubkey",
        252: "sender_gid_val",
        254: "other_gid",
        261: "my_pubkey",
        265: "chunk_len",  # not certain
        267: "plaintext",
        269: "foreign_pubkey",
        271: "crypt_chunk",  # not certain
        279: "encrypt_bytes",
        280: "subcounter",
        281: "sender_pubkey_bytes",
        282: "compressed",
        285: "group_shared_secret",
        288: "my_gid",
        292: "keypair",
        296: "gen_keypair",  # not certain
        297: "pubkey",
        298: "group_gid_val",
        299: "plaintext",
        301: "pubkey_as_compressed",
        312: "flooding_shout",
        326: "cmd_bin",
        340: "meshing",
        352: "flooding_emergency",
        353: "type_code",  # not certain
        359: "flooding_group",
        360: "flooding_private",
        375: "path",
        381: "cmd_name",
        386: "transmit_originated",
        390: "data_length",
        400: "filelike",
        464: "serialized_data",  # not certain
        465: "get_logger",
        466: "tlv_type",  # not certain
        468: "color_int",
        483: "red",
        486: "green",
        492: "expected_types",
        494: "blue",
        495: "remaining_cb",
        499: "fault_attrs",
        507: "lifetime_attrs",
        525: "decrypt_hook",
        527: "undecrypted_bytes",
        541: "keyhash",
        567: "frequency",
    }

    num = int(bits.replace("l", "0"), 2)
    name = var_names.get(num, f"v{num}")

    if prefix == "l":
        prefix = ""

    return prefix + name


with zipfile.ZipFile("goTenna-0.12.5-py3-none-any.whl") as sdk_zip:
    for filename in sdk_zip.namelist():
        if not filename.startswith("goTenna/"):
            continue

        path = filename[:filename.rindex("/")]
        os.makedirs(path, exist_ok=True)

        out_filename = re.sub(r'(__|_|l)([l1]+)_opy_', lambda x: deobfuscate_name(x.group(1), x.group(2)), filename)

        with sdk_zip.open(filename) as f:
            lines = [line.decode() for line in f.readlines()]

        with open(out_filename, "w") as f:
            try:
                index = lines.index("l1llll_opy_ = 2048\n")
                for line in lines[:index-2] + lines[index+13:]:
                    if re.search(r'^\s*(class|def) ', line):
                        line = "\n" + line
                    line = re.sub(r'l1l11l_opy_ \(u"[^"]*"\)', lambda x: eval(x.group()), line)
                    line = re.sub(r'(__|_|l)([l1]+)_opy_', lambda x: deobfuscate_name(x.group(1), x.group(2)), line)
                    f.write(line)
            except ValueError:
                for line in lines:
                    f.write(line)
