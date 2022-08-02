import argparse
from binascii import unhexlify
import codecs


parser = argparse.ArgumentParser()
parser.add_argument('input', type=str, help='Path to input file')
parser.add_argument('output', type=str, help='Path to output file')
parser.add_argument('-p', '--print', action='store_true',
                    help='Print decoded file to stdout.')
parser.add_argument('-o', '--onechar', action='store_true',
                    help='Drop semi-spaces.')

args = parser.parse_args()


charset={}
with open("IRANSYSTEM.TXT") as file:
    for line in file:
        if line.startswith("#"):
            continue

        chars=[]
        for char in line.strip().split("\t"):
            if "#" not in char:
                chars.append(char.replace("0x", ""))

        if len(chars) > 1:
            if args.onechar:
                chars[1] = chars[1].replace(
                    "0x200C", "").replace("0x200D", "").strip().split(" ")[0]
            else:
                chars[1] = chars[1].replace(" ", "")

            charset[bytes.fromhex(chars[0])]=unhexlify(
                    "".join(chars[1])).decode('utf-16-be')

file = codecs.open(args.output, "w", "utf-8")
with open(args.input, 'rb') as f:
    while True:
        c = f.read(1)
        if not c:
            break

        final_char = charset[c]
        try:
            final_char = charset[c]
        except KeyError:
            final_char = c.decode("utf-8")

        if args.print:
            print(final_char, end='')
        file.write(final_char)

file.close()
