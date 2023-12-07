def nb_cog_explore(pd, date, path, row):
        print(date)
        series = pd[(pd['date'] == date) & (pd['row'] == row)]
        # print(series)
        print("--"*40)

        print(series['red'].values[0])
        redfile = series['red'].values[0]
        index = 'index.html'
        redpre = redfile.split('/')[0:-1]
        sep = "/"
        redpre = sep.join(redpre)
        print("--"*40)

        print(redpre + sep + index)
        print("--"*40)

        cog_explorer = "https://geotiffjs.github.io/cog-explorer/#long=16.370&lat=48.210&zoom=5&scene="
        URL = cog_explorer + redpre + sep + index
        return URL

