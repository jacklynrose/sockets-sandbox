class NECProtocolEncoderDecoder:
    def __init__(self):
        # Constants for NEC protocol with noise tolerance
        self.HEADER_MARK = 9000  # Microseconds
        self.HEADER_SPACE = 4200  # Microseconds
        # Tolerance for burst length comparison (adjust as needed)
        self.TOLERANCE = 0.2  # 20% tolerance

        # Define the expected burst lengths for the NEC protocol
        self.SHORT_PULSE = 562  # Duration of short pulse
        self.SHORT_GAP = 562  # Duration of short gap
        self.LONG_GAP = 1688  # Duration of long gap

    # Function to decode a single burst into a binary value with noise tolerance
    def decode_burst(self, burst, gap):
        if abs(burst - self.SHORT_PULSE) / self.SHORT_PULSE < self.TOLERANCE and abs(gap - self.LONG_GAP) / self.LONG_GAP < self.TOLERANCE:
            return '1'  # Logical '0'
        elif abs(burst - self.SHORT_PULSE) / self.SHORT_PULSE < self.TOLERANCE and abs(gap - self.SHORT_GAP) / self.SHORT_GAP < self.TOLERANCE:
            return '0'  # Logical '1'
        else:
            # Handle noise or unknown burst
            return '?'  # Noise or unknown

    # Function to decode a list of burst lengths, considering the header
    def decode_bursts_with_header(self, burst_lengths):
        if len(burst_lengths) < 4:
            return []  # Not enough data to decode
        # Check if the header is present
        if (
            abs(burst_lengths[0] - self.HEADER_MARK) < (self.HEADER_MARK * self.TOLERANCE) and
            abs(burst_lengths[1] - self.HEADER_SPACE) < (self.HEADER_SPACE * self.TOLERANCE)
        ):
            # Remove the header from the burst_lengths list
            burst_lengths = list(burst_lengths[2:])
            # Decode the remaining bursts
            binary_data = [self.decode_burst(burst_lengths[i], burst_lengths[i + 1]) for i in range(0, len(burst_lengths) - 1, 2)]
            return binary_data
        else:
            return []  # Header not detected

    # Function to encode a binary value (0 or 1) into a burst and gap
    def encode_bit(self, bit):
        if bit == '0':
            return [self.SHORT_PULSE, self.SHORT_GAP]
        elif bit == '1':
            return [self.SHORT_PULSE, self.LONG_GAP]

    # Function to encode binary data with a header
    def encode_data(self, data):
        encoded_data = [self.HEADER_MARK, self.HEADER_SPACE]
        for bit in data:
            encoded_data += self.encode_bit(bit)
        encoded_data += [self.SHORT_PULSE]  # Add a short pulse at the end
        return encoded_data
