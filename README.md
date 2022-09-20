# Neoway Data Pirates challenge

## Script to solve test from [Neoway](https://github.com/NeowayLabs/jobs/blob/master/datapirates/challengePirates.md)

---

## Requirements to be covered

- [X] Use the https://www2.correios.com.br/sistemas/buscacep/buscaFaixaCep.cfm URL;
- [X] Get data from at least two UFs. The more, the better;
- [X] Collect all records for each UF;
- [X] Each record must contain at least 3 fields: "localidade", "faixa de cep" and a generated "id". Do not let duplicate records in your output file;
  - There are some "duplicated" but only on "localidade" because some "faixa de cep" are different between them, e.g.:
    - {"Id": "3265a9b5-1a70-4b33-a085-70b3258a5e39", "Localidade": "Rio Branco", "Faixa de CEP": " 69900-001 a 69924-999"}
    - {"Id": "7776d6cc-66e4-4c17-9530-723546e4b035", "Localidade": "Rio Branco", "Faixa de CEP": " 69900-001 a 69923-999"}
  - This kind of "duplicated" is because field that was not gathered "tipo de faixa" are different between then, the first one is "Total do município" the second one is "Exclusiva da sede urbana"
  - I just kept it because they have a little difference between them, but in a production environment we need to choose if is ok left like that, or we need one more field to differentiate between them, or just left "Total do município".
- [X] The output format must be JSONL

---

## Deliverable to be covered

- [X] The code should be sent through github with at least a README documentation explaining how to test and run it.
- [X] It would be REALLY nice if it was hosted in a git repo of your own. You can create a new empty project, create a branch and Pull Request it to the new master branch you have just created. Provide the PR URL for us so we can discuss the code 😁. BUT if you'd rather, just compress this directory and send it back to us.
  - Project will be at this [link](https://github.com/Oracy/neoway)
- [X] Do not start a Pull Request to this project.

---

## Pay Attention points

- [X] There is no right answer, we will evaluate how you solve problems and what are the results achieved.
- [X] We work mainly with Python 3 and Go, but feel free to use any language you feel more comfortable with.
  - I used python 3
- [ ] Unit tests are cool.
- [X] It's important we can execute your project, so make it clear which steps we need to follow to test and execute your project.
  - It is [here]()

---

### How to execute this scrapy

1. Clone this project to your machine
2. Go to neoway folder

```bash
cd neoway
```

3. Run command below to crawl

```bash
python3 -m scrapy crawl correios
```

---

#### Just to share

This is the project that I commented with docker, docker-compose, airflow, metabase, postgres [click here](https://github.com/Oracy/Big_Project/tree/master)
