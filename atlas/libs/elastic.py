def elastic_to_csui_format(elastic_response):
    elastic_response = elastic_response.get("hits").get("hits")
    res = []
    for i in elastic_response:
        i = i.get("_source")
        tgl_lahir = i.get('Tanggal Lahir').split("-")
        tgl_lahir.reverse()
        csui_response = {
                            "npm": i.get('NPM'),
                            "nama": i.get('Nama'),
                            "tgl_lahir": "-".join(tgl_lahir),
                            "program": [
                              {
                                "nm_org": i.get("Program Studi"),
                                "nm_prg": i.get("Jenjang"),
                                "angkatan": i.get("Angkatan"),
                                "nm_status": i.get("Status Terakhir"),
                            }]
                        }
        res.append(csui_response)
    return res
