import cherrypy
import sys
import random


class Server:
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def move(self):
        # Deal with CORS
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
        cherrypy.response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        cherrypy.response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        if cherrypy.request.method == "OPTIONS":
            return ''


        Body = cherrypy.request.json
        import random
        body = Body.get("game")
        if Body.get("players")[0] ==Body.get("you"):
            my_color = 0
        else:
            my_color = 1


        def possible_moves(b, color=0): # renvoie dico 
            directions = [[-1,0],[1,0],[0,1],[0,-1],[-1,1],[1,1],[-1,-1],[1,-1]]
            poss_moves = {} # la clé est l'emplacement actuel du pion / de la tour et la valeur est une liste des mvmts possibles
            for y in range(len(b)):
                for x in range(len(b[y])):
                    moves = [] # cette liste sert a contenir tous les mouvements possible et c'est aussi la valeur du dictionnaire poss_moves
                    if len(b[y][x])>=1 and len(b[y][x])<=4 and (b[y][x][-1])== color:
                        for dir in directions:
                            try:
                                adjacent = apply_direction(b,x,y,dir)
                                if (len(adjacent)>=1) and (len(adjacent)<=4) and ((len(b[y][x])+len(adjacent))<=5):
                                    if dir in moves:
                                        pass	
                                    else:
                                        moves.append(dir)
                            except IndexError:
                                pass
                    poss_moves[(x,y)] = moves
            return poss_moves 


        def apply_direction(b,x,y,dir): # renvoie l'emplacement du pion apres le deplacement effectué
            next_y =  y+ dir[1]
            next_x = x+ dir[0]
            if next_x <0 or next_y <0:
                raise IndexError
            return b[next_y][next_x]



        def next_move(b,my_color):# renvoie le prochain coup a jouer
            dico = possible_moves(b,my_color)
            for pos_xy,move in dico.items():
                x ,y = pos_xy[0],pos_xy[1]
                i = 0
                while i <len(move):# boucle pour parcourir les differeents coups possibles et renvoyer celui qui amene un etour à 5 éléments
                    new_len = len(b[y][x]) + len(b[y+move[i][1]][x+move[i][0]])
                    if new_len ==5:
                        return {
                                "move": {
                                        "from": [x,y],
                                        "to": [x+move[i][0],y+move[i][1]]
                                },
                                "message": "I'm Smart"
                                }
                    i +=1	
            return random_move(body,my_color)			


        def random_move(body,my_color): # renvoie un coup aléatoire
            dico = possible_moves(body,my_color)
            keys = []
            for pos_xy in dico.keys():
                keys.append(pos_xy)

            rdm = random.choice(keys)
            while len(dico[rdm])==0:
                rdm = random.choice(keys)
            x,y = rdm[0],rdm[1]
            L_val = dico[rdm]
            if len(L_val)==0:
                pass
            elif len(L_val)==1:
                return {
            "move": {
                "from": [x,y],
                "to": list(x+L_val[0], y+L_val[1])
            },
            "message": "That was a random move!"}
            else:
                rdm_val = random.choice(L_val)
                return {
                        "move": {
                                "from": [x,y],
                                "to": [x+rdm_val[0], y+rdm_val[1]]
                                },
                        "message": "That was a random move!"
                        }
        return next_move(body,my_color)

    @cherrypy.expose
    def ping(self):
        return "pong"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        port=int(sys.argv[1])
    else:
        port=8080

    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': port})
    cherrypy.quickstart(Server())