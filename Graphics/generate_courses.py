import json
import random
# Genera un conjunto de cursos ficticios con ID, nombre, créditos y prerrequisitos.
def generar_cursos(n=10000, max_prereqs=3, max_credits=4):
    cursos = []
    for i in range(1, n+1):
        # Un curso puede tener prerrequisitos solo de cursos con ID menor (para evitar ciclos)
        posibles_prereqs = list(range(1, i))
        num_prereqs = random.randint(0, min(max_prereqs, len(posibles_prereqs)))
        prereqs = random.sample(posibles_prereqs, num_prereqs) if num_prereqs > 0 else []
        curso = {
            "id": i,
            "name": f"Materia {i}",
            "credits": random.randint(1, max_credits),
            "prereqs": prereqs
        }
        cursos.append(curso)
        #print(curso)
    return cursos

if __name__ == "__main__":
    N = 10000 # cantidad de cursos a generar  
    cursos = generar_cursos(N)
    with open(f"courses_{N}.json", "w", encoding="utf-8") as f:
        json.dump(cursos, f, ensure_ascii=False, indent=2)
    print(f"Archivo courses_{N}.json generado con {N} cursos.")