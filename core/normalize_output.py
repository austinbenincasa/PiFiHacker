from clint.textui import colored


class normalize_output():

    def normalize_list(self, input):
        # turn list into string
        output = " ".join(input)
        return output.lstrip()

    def normalize_json_list(self, input):
        output = "\n"
        for el in input:
            for val in el:
                output += str(val + ": " + el[val] + "\n")

        return output

    def normalize_json(self, input):
        output = "\n"
        for el in input:
            output += str(el + ": " + input[el] + "\n")

        return output

    def normalize_wifi_table(self, input):
        print(colored.blue(
            "{:<20} {:<20} {:<8} {:<10} {:<10} {:<10}".format(
                'Name', 'Address', 'Channel', 'Encrypted', 'Type', 'Signal')))
        for el in input:
            print ("{:<20} {:<20} {:<8} {:<10} {:<10} {:<10}".format(
                el["name"],
                el["address"],
                el["channel"],
                el["encrypted"],
                el["type"],
                el["signal"]))

    def normalize_netstats_table(self, input):
        print(colored.blue("{:<20} {:<20} {:<8}".format(
            'Name', 'Address', 'Packets')))
        for el in input:
            print ("{:<20} {:<20} {:<8}".format(
                el["name"],
                el["ssid"],
                el["packets"]))
        return

    def normalize_network_map(self, input):
        print(colored.blue("{:<20} {:<20}".format(
            'IP Address', 'Mac Address')))
        for el in input:
            print ("{:<20} {:<20}".format(
                el[0],
                el[1]))

    def show_hacked_data(self, input):
        print(colored.blue("{:<25} {:<25}".format(
            'Network', 'Password')))
        for key, val in input.items():
            print ("{:<25} {:<25}".format(
                key,
                val))

    def normalize_network_scan(self, input):
        print(colored.blue("{:<20} {:<30}".format(
            'IP Address', 'Open Ports')))
        for key, val in input.iteritems():
            print ("{:<20} {:<30}".format(
                key,
                " ".join(map(str,val))))
