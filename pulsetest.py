import pulsectl

with pulsectl.Pulse('volume-checker') as pulse:
    sinks = pulse.sink_list()
    for sink in sinks:
        print(f"Sink: {sink.name}, Volume: {sink.volume.value_flat}")