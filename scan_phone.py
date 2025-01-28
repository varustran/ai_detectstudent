from scapy.all import *

def packet_handler(packet):
    if packet.haslayer(LTE_RRC):
        # Kiểm tra gói tin có chứa thông tin RRC không
        rrc_msg = packet[1]

        # Kiểm tra nếu gói tin là RRC Connection Request
        if rrc_msg.messageType == 1:
            # In ra thông tin IMEI của điện thoại
            imei = rrc_msg.ue_Identity.imei.value
            print(f"IMEI: {imei}")

            # In ra thông tin IMSI của điện thoại
            imsi = rrc_msg.ue_Identity.imsi.value
            print(f"IMSI: {imsi}")

# Bắt gói tin trên giao diện mạng di động
sniff(iface="Hehehe", prn=packet_handler, filter="udp and port 30000")

