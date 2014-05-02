import re


class BibParser:
    def __init__(self, fname):
        self.filename = fname

    def read_raw_content(self):

        item = ""
        items = []

        with open(self.filename) as f:
            while True:
                line = f.readline()
                if not line:
                    items.append(item)
                    break
                if line.startswith('@') and item:
                    items.append(item)
                    item = ""
                item += line.strip()

        return items

    def get_pre_parsed_data(self, items):
        """
        Get the pre-parsed data (tuple), with only the following values:
        (Entry_type, Entry_tag, Entry_content)
        """
        tmp_data = []
        for count, item in enumerate(items):
            r = re.match("^@.*?{", item)
            if r:
                entry_type = r.group()[1:-1]
                entry_tag = item[len(entry_type)+1:].split(",")[0][1:]

                entry_raw_content = item[len(entry_type)+len(entry_tag)+3:-1]

                tmp_data.append((entry_type, entry_tag, entry_raw_content))

        return tmp_data

    def vstrip(self, val):
        """
        Remove the following elements on a string:
        * ending comma
        * initial quote
        * ending quote
        * initial bracket
        * ending bracket
        """

        if val.endswith(","):
            val = val[:-1]
        if val.startswith("\""):
            val = val[1:]
        if val.endswith("\""):
            val = val[:-1]
        if val.startswith("{"):
            val = val[1:]
        if val.endswith("}"):
            val = val[:-1]

        return val

    def get_parsed_data(self, pparsed):
        """
        Takes the pre-parsed data and apply some last rules
        to generate a dictionary with all the information of an entry
        """
        l = []
        for ttype, tag, content in pparsed:
            d = {}

            # Information that we already have
            d["type"] = ttype
            d["tag"] = tag

            # Getting the left side of the attributes (names)
            attr_name = filter(None, re.findall("\w+\s*=", content))

            # Getting the right side of the attributes (values)
            attr_value = filter(None, re.split("\w+\s*=",   content))

            assert len(attr_name) == len(attr_value)
            for name, value in zip(attr_name, attr_value):
                # Removing the " =" substring
                n = name.strip().split()[0]

                # Removing the "," at the end, and the "" and {}
                v = self.vstrip(value.strip())

                # Adding the value
                d[n] = v

            l.append(d)
        return l
