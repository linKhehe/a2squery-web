import ipaddress
import streamlit as st
import typing
from dataclasses import asdict
from enum import Enum
from a2squery import A2SQuery # type: ignore0

@typing.no_type_check
def safe_dict_factory(data):
    safe_dict = {}
    for key, value in data:
        if isinstance(value, Enum):
            safe_dict[key] = value.name
        else:
            safe_dict[key] = value
    return safe_dict

st.set_page_config(
   page_title="A2SQuery",
   menu_items={}
)

st.title("A2SQuery")

st.text_input("Server IP:", key="server_ip")
st.number_input("Query Port:", key="server_port", min_value=1, max_value=65535, value=27015)

if st.button("Query Server"):
    server_ip = st.session_state.server_ip
    server_port = st.session_state.server_port

    if server_ip == "localhost":
        st.error("No private or loopback addresses please and thank you.")
        st.stop()
    else:
        try:
            ip = ipaddress.ip_address(server_ip)
            if ip.is_private or ip.is_loopback:
                st.error("No private or loopback addresses please and thank you.")
                st.stop()
        except ValueError:
            pass

    try:
        with A2SQuery(server_ip, server_port) as a2s:
            info = a2s.info()
            rules = a2s.rules()
            players = a2s.players()

            st.write("Info")
            st.json(asdict(info, dict_factory=safe_dict_factory)) # type: ignore
            st.write("Players")
            st.json([asdict(p, dict_factory=safe_dict_factory) for p in players]) # type: ignore
            st.write("Rules")
            st.json(rules)
    except TimeoutError:
        st.error("Timed out connecting to server.")
    except Exception as e:
        st.error(f"Failed to query the server.")
