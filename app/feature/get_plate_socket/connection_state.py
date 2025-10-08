from collections import deque

class ConnectionState:
    def __init__(self, consensus_frames=4):
        self.last_detections = deque(maxlen=consensus_frames)
        self.consensus_frames = consensus_frames

    def push(self, plate_or_none):
        self.last_detections.append(plate_or_none)

    def consensus_plate(self):
        if len(self.last_detections) < self.last_detections.maxlen:
            return None
        counts = {}
        for p in self.last_detections:
            if p is None: continue
            counts[p] = counts.get(p, 0) + 1
        if not counts:
            return None
        plate, cnt = max(counts.items(), key=lambda x: x[1])
        if cnt >= (self.last_detections.maxlen // 2) + 1:
            return plate
        return None