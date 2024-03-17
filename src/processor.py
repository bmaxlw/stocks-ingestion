from re import findall

class Processor:
    info_pattern  = r"ticker:.*name:.*nameFull:.*exchange:.*\",baseurl"
    lh52_pattern  = r"(h52:\d*\.\d*|l52:\d*\.\d*)"
    chart_pattern = r"t:\d{10},c:\d*\.\d*" 

    def __init__(self) -> None:
        self.response_dict = {}
        self.response_list = []

    # process responses provided by extractor 
    # returns consolidated dictionary with main metrics
    def process(self, responses: list[str]) -> dict[str,str]:
        for response in responses:
            info = list(filter(lambda element: element is not None, [element.split(':') if ":" in element \
                   else None for element in findall(self.info_pattern, response)[0].split(',')]))
            low_high = [element.split(":") for element in findall(self.lh52_pattern, response)]
            chart = [element.replace("t:", "").replace("c:", "").split(',') \
                    for element in findall(self.chart_pattern, response)]
            for item in info + low_high + chart:
                self.response_dict[item[0]] = item[1].replace('"', "")
            self.response_list.append(self.response_dict)
            self.response_dict = {}
        return self.response_list
