import sys

class SudokuSolver(object):
    def __init__(self, inboard):
        self.board_str = inboard
        self.digits = self.rows = "123456789"
        self.cols = "ABCDEFGHI"
        self.squares = [ci + ri for ri in self.rows for ci in self.cols]
        self.build_units()
        self.values = dict((s, self.digits) for s in self.squares)
        self.initialize_board()

    def build_units(self):
        self.units = {}
        self.peers = {}
        def populate_units_peers(group):
            for s in group:
                self.units[s] = self.units.get(s, [])
                self.units[s].append(group)
                self.peers[s] = self.peers.get(s, set())
                self.peers[s].update(group)
                self.peers[s].remove(s)
        #rows 
        for ri in self.rows:
            group = []
            for ci in self.cols:
                group.append(ci+ri)
            populate_units_peers(group)
        #cols
        for ci in self.cols:
            group = []
            for ri in self.rows:
                group.append(ci + ri)
            populate_units_peers(group)
        #squares
        for (r0, c0) in [(0, 0), (0, 3), (0, 6), (3, 0), (3,3), (3,6), (6,0), (6,3), (6,6)]:
            group = []
            for dr in xrange(3):
                for dc in xrange(3):
                    ri = self.rows[r0 + dr]
                    ci = self.cols[c0 + dc]
                    group.append(ci + ri)
            populate_units_peers(group)
        return  

    def initialize_board(self):
        for (i, si) in enumerate(self.board_str.replace(' ', '')):
            if si in self.digits and self.assign(self.values, self.squares[i], si) == False:
                raise RuntimeError("board is not valid")
        return

    def display(self, values):
        for (i, ri) in enumerate(self.rows):
            row_str_vec = [] 
            for (j, cj) in enumerate(self.cols):
                if j % 3 == 0:
                    row_str_vec.append('|')
                key = cj+ri
                if len(values[key]) == 1:
                    row_str_vec.append(values[key])
                else:
                    row_str_vec.append('.')
            if i % 3 == 0:
                print ' -' * 12
            print ' '.join(row_str_vec)
        return

    def assign(self, values, square, d):
        for vi in values[square]:
            if vi == d:
                continue
            if not self.eliminate(values, square, vi):
                return False 
        return values

    def eliminate(self, values, square, d):
        if d not in values[square]:
            return values
        values[square] = values[square].replace(d, "")
        if len(values[square]) == 0:
            return False
        #once a square is left with one choice, eliminate this choice from all of square's peers
        if len(values[square]) == 1:
            for pi in self.peers[square]:
                if not self.eliminate(values, pi, values[square]):
                    return False
        
        for ui in self.units[square]:
            sqi_w_d = [sqi for sqi in ui if d in values[sqi]]
            if len(sqi_w_d) == 1:
                if not self.assign(values, sqi_w_d[0], d):
                    return False
        return values

    def search(self, values):
        if values == False:
            return False
        cand_pairs = [ (len(cands), sqi) for (sqi, cands) in values.items() if len(cands) > 1]
        if len(cand_pairs) == 0:
            return values
        _, sq = min(cand_pairs)
        for di in values[sq]:
            new_values = self.search(self.assign(values.copy(), sq, di))
            if new_values:
                return new_values
        return False
        
    def test(self):
        print self.values
        self.display(self.values)
        values = self.search(self.values)
        if values:
            self.display(values)
        return

if len(sys.argv) > 1:
    board1 = sys.argv[1]
else:
    board1 = "400000805 030000000 000700000 020000060 000080400 000010000 000603070 500200000 104000000"
c = SudokuSolver(board1)
c.test()

