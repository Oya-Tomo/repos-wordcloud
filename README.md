# Repos Word Cloud

## description

Scrape your repositories and generate a word cloud picture from your programs.

## example

![wordcloud](assets/wordcloud.png)

## usage

### put font file

- Create `font` directory.
- Put a `ttf` file in `font` directory.

### make config.json

```json
{
  "font": "font/[putted-font].ttf",
  "repos": [
    "https://github.com/Oya-Tomo/repos-wordcloud",
    "https://github.com/..."
  ]
}
```

### run docker container

```shell
docker compose up
```

### get picture

- Generated picture will be in `export` directory.
