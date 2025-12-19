import subprocess
from pathlib import Path

gpt = Path(r"C:\Program Files\snap\bin\gpt.exe")

cmd = [
    str(gpt),
    "-J-Xmx8G",
    "-c", "6000",
    "app/services/snap_work/graphs/hercules.xml",
    "-Pinput=app/downloads/{input}",
    "-Poutput=app/services/snap_work/out/{output}",
]
def run_snap_graph(input, output):
    formatted_cmd = [arg.format(input=input, output=output) for arg in cmd]
    subprocess.run(formatted_cmd, check=True)

if __name__ == "__main__":
    run_snap_graph(
        "S1A_IW_GRDH_1SDV_20251111T081655_20251111T081724_061827_07BAAF_86E7.SAFE.zip",
        "S1A_IW_GRDH_1SDV_20251111T081655_20251111T081724_061827_07BAAF_86E7.nc"
    )