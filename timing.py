from timeit import default_timer as timer

class Timing:
    def __init__(self):
        self.timing = [('start', timer())]
    
    def mark(self, name: str):
        self.timing.append((name, timer()))
    
    def __repr__(self) -> str:
        _, start = self.timing[0]
        _, end = self.timing[-1]
        
        interval_pairs = zip(self.timing[:-1], self.timing[1:])
        intervals = [(f'  {name}', end - start) for (_, start), (name, end) in interval_pairs]
        intervals.append(('Total', end - start))
        
        width = max(len(name) for name, _ in intervals)
        lines = (f'{name.ljust(width)} {time:10.3f} s' for name, time in intervals)
        
        return '\n'.join(lines)