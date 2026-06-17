# ============================================================
#  ifm_client.py  —  Client ifm IoT Core (AL1306)
#  Chemins validés par tests PowerShell réels (05/2026)
#
#  Règle clé du protocole ifm IoT Core :
#    - Pour LIRE un datapoint  → POST avec adr = "/chemin/getdata"
#    - Pour ÉCRIRE un datapoint → POST avec adr = "/chemin/setdata"
#    - Pour les services (getdatamulti, gettree...) → POST avec adr = "/service"
# ============================================================

import requests
import json
import logging
from typing import Optional, Any

from app import config

log = logging.getLogger("ifm_client")

IFM_ENDPOINT = f"http://{config.MASTER_IP}:{config.MASTER_PORT}/iolink/v1/"

_cid_counter = 1

DEVICE_STATUS = {
    0: "non connecté",
    1: "pré-opérationnel",
    2: "opérationnel ✓",
    3: "erreur de communication"
}

PORT_MODE = {
    0: "Désactivé",
    1: "Entrée digitale (DI)",
    2: "Sortie digitale (DO)",
    3: "IO-Link"
}


def _next_cid() -> int:
    global _cid_counter
    _cid_counter += 1
    return _cid_counter


class IFMClient:

    def __init__(self):
        self.endpoint = IFM_ENDPOINT
        self.timeout  = (config.CONNECT_TIMEOUT, config.READ_TIMEOUT)
        self.session  = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        if config.USERNAME:
            self.session.auth = (config.USERNAME, config.PASSWORD)

    # ── Requête brute ────────────────────────────────────────

    def _request(self, adr: str, data: Optional[dict] = None) -> Optional[dict]:
        """
        Requête brute ifm IoT Core.
        Retourne le dict "data" de la réponse, ou None si erreur.
        """
        payload = {
            "code": "request",
            "cid":  _next_cid(),
            "adr":  adr,
            "data": data or {}
        }
        try:
            r = self.session.post(
                self.endpoint,
                data=json.dumps(payload),
                timeout=self.timeout
            )
            r.raise_for_status()
            resp = r.json()
            if resp.get("code") == 200:
                return resp.get("data")
            else:
                log.warning(f"ifm erreur {resp.get('code')} sur [{adr}] → {resp}")
                return None
        except requests.exceptions.ConnectionError:
            log.error(f"Impossible de joindre {config.MASTER_IP}:{config.MASTER_PORT}")
        except requests.exceptions.Timeout:
            log.error(f"Timeout sur [{adr}]")
        except requests.exceptions.HTTPError as e:
            log.warning(f"HTTP erreur sur [{adr}] : {e}")
        except Exception as e:
            log.error(f"Erreur inattendue sur [{adr}] : {e}")
        return None

    def _getdata(self, adr: str) -> Any:
        """
        Lecture d'un datapoint scalaire.
        Le protocole ifm requiert /getdata en suffixe pour lire une valeur.
        Retourne directement la valeur (data["value"]), pas le dict entier.
        """
        result = self._request(f"{adr}/getdata")
        if result is None:
            return None
        return result.get("value")

    # ── Infos master ─────────────────────────────────────────

    def get_master_all_info(self) -> dict:
        """Lecture groupée des infos principales du master via getdatamulti."""
        result = self._request("/getdatamulti", data={"datatosend": [
            "/deviceinfo/serialnumber/getdata",
            "/deviceinfo/productcode/getdata",
            "/deviceinfo/swrevision/getdata",
            "/deviceinfo/hwrevision/getdata",
            "/processdatamaster/temperature/getdata",
            "/processdatamaster/voltage/getdata",
            "/processdatamaster/supervisionstatus/getdata",
        ]})
        return result or {}

    def get_full_tree(self) -> Optional[dict]:
        return self._request("/gettree")

    # ── Port ─────────────────────────────────────────────────

    def get_port_mode(self, port: int) -> Optional[int]:
        """Mode du port : 0=Disabled 1=DI 2=DO 3=IO-Link"""
        return self._getdata(f"/iolinkmaster/port[{port}]/mode")

    # ── Device ───────────────────────────────────────────────

    def get_device_status(self, port: int) -> Optional[int]:
        """
        Statut IO-Link du capteur :
        0=non connecté  1=pré-op  2=opérationnel  3=erreur comms
        """
        return self._getdata(f"/iolinkmaster/port[{port}]/iolinkdevice/status")

    def get_device_identification(self, port: int) -> dict:
        """Identification complète du capteur via getdatamulti."""
        result = self._request("/getdatamulti", data={"datatosend": [
            f"/iolinkmaster/port[{port}]/iolinkdevice/vendorid/getdata",
            f"/iolinkmaster/port[{port}]/iolinkdevice/deviceid/getdata",
            f"/iolinkmaster/port[{port}]/iolinkdevice/productname/getdata",
            f"/iolinkmaster/port[{port}]/iolinkdevice/serial/getdata",
        ]})
        return result or {}

    def get_pdin(self, port: int) -> Optional[str]:
        """Process data input — valeur mesurée en hexstring (ex: '0206FD0000000000')."""
        return self._getdata(f"/iolinkmaster/port[{port}]/iolinkdevice/pdin")



    # ── Paramètres acycliques (santé) ────────────────────────

    def read_acyclic(self, port: int, index: int, subindex: int = 0) -> Optional[dict]:
        """Lecture acyclique ISDU d'un paramètre capteur."""
        return self._request(
            f"/iolinkmaster/port[{port}]/iolinkdevice/iolreadacyclic",
            data={"index": index, "subindex": subindex}
        )



    # ── Collecte complète d'un port ──────────────────────────

    def get_full_port_health(self, port: int) -> dict:
        result = {
            "port":       port,
            "port_label": f"X{port:02d}",
            "errors":     []
        }

        # 1. Mode du port
        mode_code = self.get_port_mode(port)
        mode_label = PORT_MODE.get(mode_code, f"inconnu ({mode_code})")
        result["port_mode_code"]  = mode_code
        result["port_mode_label"] = mode_label

        if mode_code != 3:
            result["connected"] = False
            result["device_status_label"] = f"Port non IO-Link ({mode_label})"
            return result

        # 2. Statut du capteur
        status_code = self.get_device_status(port)
        status_label = DEVICE_STATUS.get(status_code, f"inconnu ({status_code})")
        result["device_status_code"]  = status_code
        result["device_status_label"] = status_label
        result["connected"] = (status_code == 2)

        # 3. Identification
        ident = self.get_device_identification(port)
        if ident:
            result["identification"] = ident

        if status_code != 2:
            return result

        # 4. Process data
        pdin = self.get_pdin(port)
        if pdin is not None:
            result["pdin_hex"] = pdin
        else:
            result["errors"].append("pdin non disponible")

        # 5. Events
        events = self.get_device_events(port)
        if events is not None:
            result["iolinkevent_hex"] = events
            result["has_event"] = events not in ("0000000000000000", "00", "")
        else:
            result["errors"].append("iolinkevent non disponible")

        # 6. Paramètres de santé acycliques
        result["health_parameters"] = self.get_port_health_params(port)

        return result
