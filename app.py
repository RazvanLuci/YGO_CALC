from flask import Flask, render_template, request
from math import comb

app = Flask(__name__)

# Probabilitate exacta combinatoric
def prob_exact_k(N, S, H, k):
    if k > S or k > H:
        return 0
    return (comb(S, k) * comb(N - S, H - k)) / comb(N, H)

# Calcul probabilitati exacte + cumulative (≥k)
def build_results_cumulative(N, S, H):
    exact_probs = [round(prob_exact_k(N, S, H, k) * 100, 2) for k in range(0, H + 1)]
    cumulative_probs = {}
    for k in range(1, H + 1):
        cumulative_probs[k] = round(sum(exact_probs[k:]), 2)
    return exact_probs, cumulative_probs

@app.route("/", methods=["GET", "POST"])
def index():
    results = {}
    if request.method == "POST":
        N = int(request.form.get("deck_size", 40))
        H = int(request.form.get("hand_size", 5))

        # Starters
        if "calc_starters" in request.form:
            starters_input = request.form.get("starters", "12")
            starters_list = [int(x.strip()) for x in starters_input.split(",") if x.strip().isdigit() and int(x.strip()) > 0]
            if starters_list:
                results["starter"] = {}
                for s in starters_list:
                    exact, cumulative = build_results_cumulative(N, s, H)
                    results["starter"][s] = {"exact": list(enumerate(exact)), "cumulative": cumulative}

        # Hand Traps
        if "calc_ht" in request.form:
            ht_input = request.form.get("non_engine", "9")
            ht_list = [int(x.strip()) for x in ht_input.split(",") if x.strip().isdigit() and int(x.strip()) > 0]
            if ht_list:
                results["ht"] = {}
                for h in ht_list:
                    exact, cumulative = build_results_cumulative(N, h, H)
                    results["ht"][h] = {"exact": list(enumerate(exact)), "cumulative": cumulative}

        # Engine Requirements
        if "calc_engine" in request.form:
            engine_input = request.form.get("engine", "3")
            engine_list = [int(x.strip()) for x in engine_input.split(",") if x.strip().isdigit() and int(x.strip()) > 0]
            if engine_list:
                results["engine"] = {}
                for e in engine_list:
                    exact, cumulative = build_results_cumulative(N, e, H)
                    results["engine"][e] = {"exact": list(enumerate(exact)), "cumulative": cumulative}

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
