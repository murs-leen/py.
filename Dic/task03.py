class DengueFever:
    threshold = 15

    symptoms_weights = {
        "fever": 4,
        "headache": 2,
        "eyePain": 3,
        "rash": 5,
        "nausea": 1,
        "vomiting": 3,
        "musclePain": 2
    }

    def __init__(self, fever, headache, eyePain, rash, nausea, vomiting, musclePain):
        self.fever = fever
        self.headache = headache
        self.eyePain = eyePain
        self.rash = rash
        self.nausea = nausea
        self.vomiting = vomiting
        self.musclePain = musclePain

    def total_score(self):
        return (
            self.fever * self.symptoms_weights["fever"] +
            self.headache * self.symptoms_weights["headache"] +
            self.eyePain * self.symptoms_weights["eyePain"] +
            self.rash * self.symptoms_weights["rash"] +
            self.nausea * self.symptoms_weights["nausea"] +
            self.vomiting * self.symptoms_weights["vomiting"] +
            self.musclePain * self.symptoms_weights["musclePain"]
        )

    def is_high_risk(self):
        return self.total_score() >= self.threshold


print("\nCollecting patient record:\n")

f = input("Do you have fever? (yes/no): ")
h = input("Do you have headache? (yes/no): ")
e = input("Do you have eye pain? (yes/no): ")
r = input("Do you have rash? (yes/no): ")
n = input("Do you have nausea? (yes/no): ")
v = input("Do you have vomiting? (yes/no): ")
m = input("Do you have muscle pain? (yes/no): ")

f = 1 if f == "yes" else 0
h = 1 if h == "yes" else 0
e = 1 if e == "yes" else 0
r = 1 if r == "yes" else 0
n = 1 if n == "yes" else 0
v = 1 if v == "yes" else 0
m = 1 if m == "yes" else 0

patient = DengueFever(f, h, e, r, n, v, m)

print("Total Score:", patient.total_score())

if patient.is_high_risk():
    print('''Based on your symptoms it is possiblity that you may have Dengue.
          It is important to consult wiht a healthcare professional for further guidance.''')
else:
    print('''Based on your symptoms, it is less likely that you have Dengue.
    However, if you have concerns, it is always a good idea to consult with a healthcare professional.''')
