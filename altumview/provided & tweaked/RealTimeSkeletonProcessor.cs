public class RealTimeSkeletonProcessor
{
	private List<SkeletonModel> _frame = new List<SkeletonModel>();

	private struct SkeletonModel
    {
	// get tracker id, person id, x coords, y coords
        int TrackerId { get; set; }
        int PersonId { get; set; }
        List<float> XCoords { get; set; }
        List<float> YCoords { get; set; }
    }

// pass frame number and people detected
	private void StoreFrame(byte[] data)
	{
		var frameNum = 0;
		var numOfPeople = 0;

		var frameNumHex = string.Empty;
		for (int i = 3; i >= 0; i--)
		{
			byte curr = data[i];
			frameNumHex += curr.ToString("X2");
		}
		frameNum = Int32.Parse(frameNumHex, System.Globalization.NumberStyles.HexNumber);
// get updated frame number
		if (frameNum > _lastFrameNum)
		{
			_lastFrameNum = frameNum;
		}
		else
		{
			return;
		}

		var numOfPeopleHex = string.Empty;
		for (int i = 7; i >= 4; i--)
		{
			byte curr = data[i];
			numOfPeopleHex += curr.ToString("X2");
		}
		numOfPeople = Int32.Parse(numOfPeopleHex, System.Globalization.NumberStyles.HexNumber);

// process each person's skeletal data

		for (int i = 0; i < numOfPeople; i++)
		{
			var startIndex = 8 + (152 * i);
			var endIndex = startIndex + 152;
			var personId = -1;
			var trackerId = -1;
			var xyCoords = new List<float>();
// get tracker ID and person ID
			var personIdHex = string.Empty;
			for (int j = startIndex + 3; j >= startIndex; j--)
			{
				byte curr = data[j];
				personIdHex += curr.ToString("X2");
			}
			personId = Int32.Parse(personIdHex, System.Globalization.NumberStyles.HexNumber);

			var trackerIdHex = string.Empty;
			for (int j = startIndex + 7; j >= startIndex + 4; j--)
			{
				byte curr = data[j];
				trackerIdHex += curr.ToString("X2");
			}
			trackerId = Int32.Parse(trackerIdHex, System.Globalization.NumberStyles.HexNumber);

// get x and y coordinates, convert to float

			for (int j = startIndex + 8; j < endIndex; j = j + 4)
			{
				var coordHex = string.Empty;
				for (int k = j + 3; k >= j; k--)
				{
					byte curr = data[k];
					coordHex += curr.ToString("X2");
				}
				uint num = uint.Parse(coordHex, System.Globalization.NumberStyles.AllowHexSpecifier);

				byte[] floatVals = BitConverter.GetBytes(num);
				float coord = BitConverter.ToSingle(floatVals, 0);
				xyCoords.Add(coord);
			}
// skeleton model with the parsed data.
			var skeleton = new SkeletonModel
			{
				TrackerId = trackerId,
				PersonId = personId,
				XCoords = xyCoords.GetRange(0, 18),
				YCoords = xyCoords.GetRange(18, 18)
			};

			_frame.Add(skeleton);
		}
	}
    public static void Main(string[] args)
    {
        var data = File.ReadAllBytes("skeleton.bin");
        var processor = new RealTimeSkeletonProcessor();
        processor.StoreFrame(data);
    }
}