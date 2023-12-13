class GrammaticalRelation():

    def get_grammatical_relation(self, line):
        tokens = line.split(" ")
        if tokens[0] == "TOUR":
            rel = self.get_tour_relation(tokens[1], tokens[2])
        elif tokens[0] == "DTIME":
            rel = self.get_dtime_relation(tokens[1], tokens[2], tokens[3] + " " + tokens[4])
        elif tokens[0] == "ATIME":
            rel = self.get_atime_relation(tokens[1], tokens[2], tokens[3] + " " + tokens[4])
        elif tokens[0] == "RUN-TIME":
            rel = self.get_runtime_relation(tokens[1], tokens[2], tokens[3], tokens[4] + " " + tokens[5])
        else: # tokens[0] == "BY":
            rel = self.get_transport_relation(tokens[1], tokens[2])
        return rel


    def get_tour_relation(self, tour, city_name):
        _pred = '(s PRED GO)'
        _lobj = '(s LOBJ (TOUR t "{}"))'.format(tour)
        _to = '(s TO (CITY-NAME cn "{}"))'.format(city_name)
        return _pred + _lobj + _to


    def get_dtime_relation(self, tour, city_code, dtime):
        _pred = '(s PRED DEPART)'
        _lobj = '(s LOBJ (TOUR t "{}"))'.format(tour)
        _from = '(s FROM (CITY-CODE cc "{}"))'.format(city_code)
        _at = '(s AT (DTIME d {}))'.format(dtime)
        return _pred + _lobj + _from + _at


    def get_atime_relation(self, tour, city_code, atime):
        _pred = '(s PRED ARRIVE)'
        _lobj = '(s LOBJ (TOUR t "{}"))'.format(tour)
        _to = '(s TO (CITY-CODE cc "{}"))'.format(city_code)
        _at = '(s AT (ATIME a {}))'.format(atime)
        return _pred + _lobj + _to + _at


    def get_runtime_relation(self, tour, from_city_code, to_city_code, runtime):
        _pred = '(s PRED TRAVEL)'
        _lobj = '(s LOBJ (TOUR t "{}"))'.format(tour)
        _from = '(s FROM (CITY-CODE ccf "{}"))'.format(from_city_code)
        _to = '(s TO (CITY-CODE cct "{}"))'.format(to_city_code)
        _for = '(s FOR (RUN-TIME r "{}"))'.format(runtime)
        return _pred + _lobj + _from + _to + _for


    def get_transport_relation(self, tour, transport):
        _pred = '(s PRED TRAVEL)'
        _lobj = '(s LOBJ (TOUR t "{}"))'.format(tour)
        _by = '(s BY (TRANSPORT ts "{}"))'.format(transport)
        return _pred + _lobj + _by