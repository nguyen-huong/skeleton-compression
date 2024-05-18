import struct
import matplotlib.pyplot as plt

class RealTimeSkeletonProcessor:
    def __init__(self):
        self.frames = []
        self.frame_duration = 1/30  

    def store_frame(self, filename):
        with open(filename, 'rb') as f:
            while True:
                header_data = f.read(8)
                if len(header_data) < 8:
                    break

                frame_num, num_of_people = struct.unpack(">2I", header_data)
                
                for _ in range(num_of_people):
                    person_data = f.read(8)
                    if len(person_data) < 8:
                        break
                    
                    person_id, tracker_id = struct.unpack(">2I", person_data)
                    xy_coords_data = f.read(144)  # 18 * 2 * 4 bytes for X, Y coordinates
                    if len(xy_coords_data) < 144:
                        break

                    xy_coords = [struct.unpack(">f", xy_coords_data[i:i+4])[0] for i in range(0, len(xy_coords_data), 4)]
                    
                    x_coords = xy_coords[:18]
                    y_coords = xy_coords[18:]
                    
                    self.frames.append({
                        "FrameNum": frame_num,
                        "PersonId": person_id,
                        "TrackerId": tracker_id,
                        "XCoords": x_coords,
                        "YCoords": y_coords
                    })

    def plot_coordinates(self):
        total_duration = self.frames[-1]["FrameNum"] * self.frame_duration
        time_intervals = [i * self.frame_duration for i in range(len(self.frames))]

        for i in range(18):
            x_coords = [frame["XCoords"][i] for frame in self.frames]
            y_coords = [frame["YCoords"][i] for frame in self.frames]

            plt.figure()
            plt.plot(time_intervals, x_coords, label=f'Joint {i+1} X')
            plt.title(f'Joint {i+1} X Coordinate Over Time')
            plt.xlabel('Frame Interval')
            plt.ylabel('X Coordinate')
            plt.legend()
            plt.savefig(f'Joint_{i+1}_X.png')

            plt.figure()
            plt.plot(time_intervals, y_coords, label=f'Joint {i+1} Y')
            plt.title(f'Joint {i+1} Y Coordinate Over Time')
            plt.xlabel('Frame Interval')
            plt.ylabel('Y Coordinate')
            plt.legend()
            plt.savefig(f'Joint_{i+1}_Y.png')


processor = RealTimeSkeletonProcessor()
processor.store_frame("combined_data.dat")
processor.plot_coordinates()
