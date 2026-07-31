from functools import *
from collections import *
from itertools import *
from math import *
from statistics import *
from builtins import pow
import pyperclip
import operator
from icecream import ic
from timer_utils import timefunction
import matplotlib.pyplot as plt
from construct import *
#import binascii

from aoc_utils import * # this includes adding c:\ut to sys.path
from Utilities import *
import seq_extensions # these extend PyFunctional seq objects, don't need to directly use anything in it

Packet = namedtuple("Packet", "V,T,body,bits_used,extra")


def run(inp, is_real):
    ics = nothing if is_real else ic
    print_result = partial(print_result_aoc, is_real)

    inp = inp.strip().split('\n')
    message = inp[0]
#    message = inp[0].encode()
    ic(message)
#    ics(Hex(GreedyBytes).parse(message))
#    ics(binascii.unhexlify(message))
    message_bytes = bytes.fromhex(message)
#    ics(message_bytes)
    as_bin = "".join(format(b, '08b') for b in message_bytes)
#    ics(as_bin, len(as_bin))
#    ics(["".join(str(b) for b in chunk) for chunk in chunks_of_n(as_bin, 4)])

    def next_int(n_bits, bit_string):
        return int(bit_string[:n_bits], 2), bit_string[n_bits:]

    def next_string(n_bits, bit_string):
        return bit_string[:n_bits], bit_string[n_bits:]


    def parse_packets(bit_string, level=0, num_packets = 10**5, out = print):
#        ics(num_packets, bit_string)
        indent = "|       " * level
#        ic(level, num_packets, len(bit_string))
        if num_packets:
            out(f"{indent}parse_packets: num_packets={num_packets}, len={len(bit_string)}")
        else:
            out(f"{indent}parse_packets: len={len(bit_string)}")

        cur_packets = []
        consumed = 0
        n_packet = 0
        fun_starting_len = len(bit_string)
        bits_used = 0

            # need 6 bits for version and type, then at least 5 for numebr or 12 for operator
            # however trailing zero bits shouldn't exceed 7 from hex number
        while len(bit_string) > 7 and len(cur_packets) < num_packets:
            starting_length = len(bit_string)
            out(f"{indent}| {n_packet}: start={starting_length}, con={consumed}")
#            ic(level, n_packet, starting_length, consumed)
            V, bit_string = next_int(3, bit_string)
            T, bit_string = next_int(3, bit_string)
            base_bits_used = 6
            out(f"{indent}|    V={V}, T={T}: ", end="")

            if T == 4:
                number_string = ""
#                ics(list(chunks_of_n(bit_string, 5)))

                while True:
                    more, bit_string = next_int(1, bit_string)
                    chunk, bit_string = next_string(4, bit_string)
#                    ics(more, chunk)
                    number_string += chunk

                    if not more:
                        break

                number = int(number_string, 2)
#                ic(V, T, number_string, number)
                out(number)
                local_bits_used = (len(number_string) // 4) * 5
                cur_packets.append(Packet(V, T, number, base_bits_used + local_bits_used, f"num_bits={local_bits_used}"))
            else:
                type_id, bit_string = next_int(1, bit_string)
                base_bits_used += 1
#                ics(V, T, type_id, bit_string)
#                ic(V, T, type_id)
                out(f"type_id={type_id}, ", end="")

                if type_id:
                    need_num_packets, bit_string = next_int(11, bit_string)
                    base_bits_used += 11
                    out(f"need_num_packets={need_num_packets}")
#                    ic(V, T, type_id, need_num_packets)
                    new_packet, local_bits_used, bit_string = parse_packets(bit_string, level+1, need_num_packets, out)
#                    ic(V, T, type_id, need_num_packets, len(bit_string))
                    cur_packets.append(Packet(V, T, new_packet, base_bits_used + local_bits_used, f"need_num_packets={need_num_packets}"))
                else:
                    num_bits, bit_string = next_int(15, bit_string)
                    base_bits_used += 15
                    out(f"num_bits={num_bits}")
                    new_packet, local_bits_used, _ = parse_packets(bit_string[:num_bits], level+1, out=out)
#                    ic(V, T, type_id, num_bits)
                    bit_string = bit_string[num_bits:]
#                    ic(V, T, type_id, num_bits, len(bit_string))
                    cur_packets.append(Packet(V, T, new_packet, base_bits_used + local_bits_used, f"num_bits={num_bits}"))

            bits_used += base_bits_used + local_bits_used
            ending_length = len(bit_string)
            consumed += starting_length - ending_length
            out(f"{indent}|    start={starting_length}, end={ending_length}, con={consumed}, bits_used={bits_used}")
#            ic(level, n_packet, starting_length, ending_length, consumed)
            n_packet += 1

        if len(cur_packets) >= num_packets:
            out(f"{indent}Stopped loop because len(cur_packets) ({len(cur_packets)}) >= num_packets ({num_packets})")
        else:
            out(f"{indent}Stopped loop because ran out of bits ({len(bit_string)}).")


        fun_ending_len = len(bit_string)
        out(f"{indent}func consumed: {consumed}, func starting: {fun_starting_len}, func ending: {fun_ending_len}")
        return cur_packets, bits_used, bit_string

    bit_string = as_bin
    packets, bits_used, _ = parse_packets(bit_string, out = nothing)
#    ic(bits_used)
#    ics(packets)


    def packet_repr(packets, level=0):
        build = ""
        indent = "    " * level

        for packet in packets:
            build += f"{indent}{packet.V}, {packet.T}: "

            if packet.T == 4:
                build += f"{packet.body}, bits_used={packet.bits_used} ({packet.extra})\n"
            else:
                build += f"bits_used={packet.bits_used} ({packet.extra})\n" + packet_repr(packet.body, level + 1)

        return build

    def sum_versions(packets):
        total = 0

        for packet in packets:
            total += packet.V

            if packet.T != 4:
                total += sum_versions(packet.body)

#            ics(total)
#            ics(packet)

        return total

#    ic(packet_repr(packets))
#    ic(sum_versions(packets))


    @timefunction
    def part1():
        result = sum_versions(packets)
        print_result(result)

    def eval_packets(packets):
        values = []

        for packet in packets:
            if packet.T == 4:
                value = packet.body
            else:
                sub_values = eval_packets(packet.body)

                if packet.T == 0:
                    value = sum(sub_values)
                elif packet.T == 1:
                    value = reduce(operator.mul, sub_values)
                elif packet.T == 2:
                    value = min(sub_values)
                elif packet.T == 3:
                    value = max(sub_values)
                elif packet.T == 5:
                    value = sub_values[0] > sub_values[1]
                elif packet.T == 6:
                    value = sub_values[0] < sub_values[1]
                elif packet.T == 7:
                    value = sub_values[0] == sub_values[1]

            values.append(int(value))

#            ics(total)
#            ics(packet)

        return values

    def part2():
        result = eval_packets(packets)[0]
        print_result(result)


    part1()
    part2()

def main():
#    print("Sample:")
#    run(samp_inp, False)

    for samp_inp in samp_inps:
        print("Sample:")
        run(samp_inp, False)

    print("Actual:")
    run(real_inp, True)




samp_inp = r"""
620080001611562C8802118E34

"""
samp_inps = [
    r"8A004A801A8002F478",
    r"620080001611562C8802118E34",
    r"C0015000016115A2E0802F182340",
    r"A0016C880162017C3686B18A3D4780",
    ]

samp_inps = [
    r"C200B40A82",
    r"04005AC33890",
    r"880086C3E88112",
    r"CE00C43D881120",
    r"D8005AC2A8F0",
    r"F600BC2D8F",
    r"9C005AC2F8F0",
    r"9C0141080250320F1802104A08",
    ]


samp_inp_op_num_bits = r"""
38006F45291200

"""

samp_inp_op_num_packets = r"""
EE00D40C823060
"""

samp_inp_lit = r"D2FE28"


real_inp = r"""
20546718027401204FE775D747A5AD3C3CCEEB24CC01CA4DFF2593378D645708A56D5BD704CC0110C469BEF2A4929689D1006AF600AC942B0BA0C942B0BA24F9DA8023377E5AC7535084BC6A4020D4C73DB78F005A52BBEEA441255B42995A300AA59C27086618A686E71240005A8C73D4CF0AC40169C739584BE2E40157D0025533770940695FE982486C802DD9DC56F9F07580291C64AAAC402435802E00087C1E8250440010A8C705A3ACA112001AF251B2C9009A92D8EBA6006A0200F4228F50E80010D8A7052280003AD31D658A9231AA34E50FC8010694089F41000C6A73F4EDFB6C9CC3E97AF5C61A10095FE00B80021B13E3D41600042E13C6E8912D4176002BE6B060001F74AE72C7314CEAD3AB14D184DE62EB03880208893C008042C91D8F9801726CEE00BCBDDEE3F18045348F34293E09329B24568014DCADB2DD33AEF66273DA45300567ED827A00B8657B2E42FD3795ECB90BF4C1C0289D0695A6B07F30B93ACB35FBFA6C2A007A01898005CD2801A60058013968048EB010D6803DE000E1C6006B00B9CC028D8008DC401DD9006146005980168009E1801B37E02200C9B0012A998BACB2EC8E3D0FC8262C1009D00008644F8510F0401B825182380803506A12421200CB677011E00AC8C6DA2E918DB454401976802F29AA324A6A8C12B3FD978004EB30076194278BE600C44289B05C8010B8FF1A6239802F3F0FFF7511D0056364B4B18B034BDFB7173004740111007230C5A8B6000874498E30A27BF92B3007A786A51027D7540209A04821279D41AA6B54C15CBB4CC3648E8325B490401CD4DAFE004D932792708F3D4F769E28500BE5AF4949766DC24BB5A2C4DC3FC3B9486A7A0D2008EA7B659A00B4B8ACA8D90056FA00ACBCAA272F2A8A4FB51802929D46A00D58401F8631863700021513219C11200996C01099FBBCE6285106
"""

main()

