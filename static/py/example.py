try:
        with open(path + datetime.datetime.now().strftime("%Y-%m-%d") + name, "a") as f:
            line = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S") + " " + text + "\n"
            f.write(line)

    finally:
        f.close()