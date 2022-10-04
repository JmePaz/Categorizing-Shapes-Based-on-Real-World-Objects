class PlayerScore:
    def __init__(self, score, total, txtLbl):
        self.score = score
        self.total = total
        self.txtLbl = txtLbl

    def gain_points(self):
        #changing score
        self.score += 1
        #configuring the txtlbl
        self.txtLbl.configure(text=f"Points: {self.score}")

    def is_full_score(self):
        return self.score == self.total
    