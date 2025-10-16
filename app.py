from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def round_robin(processes, burst_time, quantum):
    n = len(processes)
    remaining_bt = burst_time[:]
    waiting_time = [0] * n
    t = 0

    while True:
        done = True
        for i in range(n):
            if remaining_bt[i] > 0:
                done = False
                if remaining_bt[i] > quantum:
                    t += quantum
                    remaining_bt[i] -= quantum
                else:
                    t += remaining_bt[i]
                    waiting_time[i] = t - burst_time[i]
                    remaining_bt[i] = 0
        if done:
            break

    turnaround_time = [burst_time[i] + waiting_time[i] for i in range(n)]
    return waiting_time, turnaround_time

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    processes = data['processes']
    burst_times = [int(x) for x in data['burstTimes']]
    quantum = int(data['quantum'])

    waiting_time, turnaround_time = round_robin(processes, burst_times, quantum)

    avg_wait = sum(waiting_time) / len(waiting_time)
    avg_turn = sum(turnaround_time) / len(turnaround_time)

    return jsonify({
        'waiting_time': waiting_time,
        'turnaround_time': turnaround_time,
        'avg_wait': avg_wait,
        'avg_turn': avg_turn
    })

if __name__ == '__main__':
    app.run(debug=True)
