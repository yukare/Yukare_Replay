init python:

    # Função chamada para exibir síncronamente/modalmente a janela de detalhes do passo
    def guide(pessoa, passo, descricao, requerimentos=None):
        renpy.call_screen("yukare_guide_detail", person=pessoa, step=passo, description=descricao, requirements=requerimentos)


# Tela principal de seleção do guia
screen yukare_guide_selection():
    modal True
    zorder 150

    # Fundo escurecido semitransparente
    add Solid("#090b11e6")

    # Painel central principal
    frame:
        align (0.5, 0.5)
        xysize (1240, 680)
        background Frame("Yukare_Guide/images/frame.png", Borders(4, 4, 4, 4))
        padding (20, 20, 20, 20)

        vbox:
            spacing 15

            # Cabeçalho da janela
            hbox:
                xfill True
                text "PROGRESSION GUIDE" color "#38bdf8" size 32 bold True yalign 0.5
                textbutton "CLOSE" action Hide("yukare_guide_selection") align (1.0, 0.5) text_color "#ef4444" text_size 24 text_hover_color "#f87171"

            # Layout principal dividido em duas colunas
            hbox:
                spacing 40
                xfill True
                yfill True

                # Painel Esquerdo: Lista de Personagens
                frame:
                    xysize (350, 580)
                    background Frame("Yukare_Guide/images/frame.png", Borders(4, 4, 4, 4))
                    padding (15, 15)

                    vbox:
                        spacing 15
                        xfill True
                        text "CHARACTERS" color "#94a3b8" size 20 bold True
                        null height 10

                        viewport:
                            scrollbars "vertical"
                            mousewheel True
                            draggable True
                            xfill True
                            yfill True

                            vbox:
                                spacing 10
                                for char_key, char_data in yukare_guide_steps.items():
                                    $ char_name = char_data["name"].strip(")")
                                    textbutton char_name:
                                        action SetVariable("yukare_selected_char", char_key)
                                        xfill True
                                        ysize 50
                                        background (Frame("Yukare_Guide/images/hover_background.png", Borders(4, 4, 4, 4)) if (yukare_selected_char == char_key) else None)
                                        text_color ("#38bdf8" if (yukare_selected_char == char_key) else "#ffffff")
                                        text_hover_color "#38bdf8"
                                        text_size 18
                                        left_padding 15

                # Painel Direito: Lista de Passos do Personagem Selecionado
                frame:
                    xysize (810, 580)
                    background Frame("Yukare_Guide/images/frame.png", Borders(4, 4, 4, 4))
                    padding (20, 20)

                    vbox:
                        spacing 15
                        xfill True
                        yfill True

                        if yukare_selected_char:
                            $ selected_data = yukare_guide_steps.get(yukare_selected_char, None)
                            if selected_data:
                                $ clean_name = selected_data["name"].strip(")")
                                text "STEPS FOR: " + clean_name.upper() color "#94a3b8" size 20 bold True
                                null height 10

                                viewport:
                                    scrollbars "vertical"
                                    mousewheel True
                                    draggable True
                                    xfill True
                                    yfill True

                                    vbox:
                                        spacing 12
                                        xsize 740
                                        for step_num, step_data in selected_data["steps"].items():
                                            $ step_title = step_data["title"]
                                            $ label_name = "{}_{}".format(selected_data["label_prefix"], step_num)
                                            $ done_val = str(step_data.get("done", "false")).lower()
                                            $ border_color = "#a855f7" if done_val == "info" else ("#22c55e" if done_val in ("true", "1") else "#3b82f6")
                                            $ step_bg = Frame(im.MatrixColor("Yukare_Guide/images/frame.png", im.matrix.saturation(0.0) * im.matrix.colorize("#000000", border_color)), Borders(4, 4, 4, 4))


                                            button:
                                                if renpy.has_label(label_name):
                                                    action Call(label_name)
                                                else:
                                                    action NullAction()

                                                xfill True
                                                ysize 85
                                                background step_bg
                                                padding (15, 10)

                                                hbox:
                                                    xfill True
                                                    yalign 0.5

                                                    # Círculo com o número do passo
                                                    frame:
                                                        xysize (40, 40)
                                                        background Frame("Yukare_Guide/images/bubble.png", Borders(4, 4, 4, 4))
                                                        yalign 0.5
                                                        text step_num align (0.5, 0.5) color "#000" size 18 bold True

                                                    # Informações do passo
                                                    vbox:
                                                        xoffset 15
                                                        yalign 0.5
                                                        text step_title color "#ffffff" size 18 bold True
                                                        if not renpy.has_label(label_name):
                                                            text "(Step unavailable - Label not declared)" color "#ef4444" size 12
                                                        else:
                                                            text "Click to view details" color "#a1a1aa" size 12
                            else:
                                text "Select a character from the list to view the guide." color "#a1a1aa" size 20 align (0.5, 0.5) text_align 0.5
                        else:
                            text "Select a character from the list to view the guide." color "#a1a1aa" size 20 align (0.5, 0.5) text_align 0.5


# Tela modal para exibição dos detalhes de um passo específico
screen yukare_guide_detail(person, step, description, requirements):
    modal True
    zorder 200

    # Retrieve data from the dictionary dynamically
    python:
        person_key = person.lower().strip(")")
        step_dict = None
        if person_key in yukare_guide_steps:
            step_dict = yukare_guide_steps[person_key]["steps"].get(step, None)

        real_title = ""
        real_description = ""
        real_location = ""
        real_requirements = ""

        if step_dict:
            real_title = step_dict.get("title", "")
            real_description = step_dict.get("description", "")
            real_location = step_dict.get("location", "")
            reqs_val = step_dict.get("requirements", "")
            if isinstance(reqs_val, (list, tuple)):
                non_empty_reqs = [r for r in reqs_val if r]
                real_requirements = ", ".join(non_empty_reqs) if non_empty_reqs else "None"
            else:
                real_requirements = reqs_val if reqs_val else "None"
        else:
            real_title = description
            real_description = description
            real_requirements = requirements if requirements else "None"

    # Fundo escurecido para focar os detalhes
    add Solid("#000000a6")

    # Janela de Detalhes
    frame:
        align (0.5, 0.5)
        xysize (800, 560)
        background Frame("Yukare_Guide/images/frame.png", Borders(4, 4, 4, 4))
        padding (40, 30, 40, 30)

        vbox:
            xfill True
            yfill True
            spacing 18

            # Cabeçalho da janela
            hbox:
                xfill True
                vbox:
                    $ char_display_name = yukare_guide_steps[person_key]["name"].strip(")") if person_key in yukare_guide_steps else person.strip(")")
                    text "Progression Guide - " + char_display_name color "#38bdf8" size 24 bold True
                    text "Step " + step + " - " + real_title color "#94a3b8" size 16 bold True

                textbutton "X" action Return() align (1.0, 0.0) text_color "#ef4444" text_size 28 text_hover_color "#f87171"

            # Divisor horizontal
            frame:
                xfill True
                ysize 2
                background "#334155"

            # Descrição do que fazer
            vbox:
                spacing 6
                text "WHAT TO DO:" color "#38bdf8" size 16 bold True
                text real_description color "#f8fafc" size 18 line_spacing 4

            # Localização do passo
            if real_location:
                vbox:
                    spacing 6
                    text "LOCATION:" color "#38bdf8" size 16 bold True
                    text real_location color "#f8fafc" size 18

            # Requisitos do passo
            vbox:
                spacing 6
                text "REQUIREMENTS:" color "#eab308" size 16 bold True
                text real_requirements color "#f8fafc" size 18

            # Espaçador
            null height 10

            # Botão fechar
            textbutton "GOT IT":
                action Return()
                align (0.5, 1.0)
                background Frame("Yukare_Guide/images/hover_background.png", Borders(4, 4, 4, 4))
                padding (40, 10)
                text_color "#ffffff"
                text_hover_color "#38bdf8"
                text_size 20
                text_bold True


# Tela modal para exibição de status e relações dos personagens
screen yukare_status_screen():
    modal True
    zorder 150

    # Fundo escurecido semitransparente
    add Solid("#090b11e6")

    # Painel central
    frame:
        align (0.5, 0.5)
        xysize (950, 620)
        background Frame("Yukare_Guide/images/frame.png", Borders(4, 4, 4, 4))
        padding (25, 25, 25, 25)

        vbox:
            spacing 20
            xfill True

            # Cabeçalho
            hbox:
                xfill True
                text "CHARACTER STATUS & STATS" color "#38bdf8" size 30 bold True yalign 0.5
                textbutton "CLOSE" action Hide("yukare_status_screen") align (1.0, 0.5) text_color "#ef4444" text_size 22 text_hover_color "#f87171"

            # Linha divisória
            frame:
                xfill True
                ysize 2
                background "#334155"

            # Layout principal dividido em duas colunas
            hbox:
                spacing 40
                xfill True

                # Painel Esquerdo: Info do Jogo e Outras Relações
                vbox:
                    xsize 410
                    spacing 20

                    # Estatísticas Gerais do Jogo
                    frame:
                        xfill True
                        padding (20, 20)
                        background Solid("#1e293b80")
                        vbox:
                            spacing 10
                            text "GAME STATS" color "#38bdf8" size 18 bold True
                            null height 5
                            hbox:
                                text "Time: " color "#94a3b8" size 16
                                text "[Hour]:00" color "#f8fafc" size 16 bold True
                            hbox:
                                text "Day: " color "#94a3b8" size 16
                                text "[dayname] (Day [day])" color "#f8fafc" size 16 bold True
                            hbox:
                                text "Cash: " color "#94a3b8" size 16
                                text "$[mny]" color "#22c55e" size 16 bold True

                    # Relações Secundárias
                    frame:
                        xfill True
                        padding (20, 20)
                        background Solid("#1e293b80")
                        vbox:
                            spacing 12
                            text "OTHER RELATIONSHIPS" color "#38bdf8" size 18 bold True
                            null height 5
                            hbox:
                                text "Elaine: " color "#94a3b8" size 16
                                text "[erel]" color "#f59e0b" size 16 bold True
                            hbox:
                                text "Melinda: " color "#94a3b8" size 16
                                text "[melrel]" color "#f59e0b" size 16 bold True

                # Painel Direito: Personagens Principais (Mãe e Irmã)
                vbox:
                    xsize 450
                    spacing 20

                    # Status da Mãe (Jenny)
                    frame:
                        xfill True
                        padding (20, 20)
                        background Solid("#1e293b80")
                        vbox:
                            spacing 10
                            text "[mname] (Jenny)" color "#ff86c2" size 20 bold True
                            
                            vbox:
                                spacing 4
                                hbox:
                                    xfill True
                                    text "Relationship" color "#94a3b8" size 14
                                    text "[mrel]/500" color "#38bdf8" size 14 bold True xalign 1.0
                                bar value mrel range 500 xsize 410 ysize 12

                            hbox:
                                text "Corruption: " color "#94a3b8" size 14
                                text "[mcorr]/50" color "#a855f7" size 14 bold True

                    # Status da Irmã (Nadia)
                    frame:
                        xfill True
                        padding (20, 20)
                        background Solid("#1e293b80")
                        vbox:
                            spacing 10
                            text "[sname] (Nadia)" color "#ff86c2" size 20 bold True
                            
                            vbox:
                                spacing 4
                                hbox:
                                    xfill True
                                    text "Relationship" color "#94a3b8" size 14
                                    text "[srel]/500" color "#38bdf8" size 14 bold True xalign 1.0
                                bar value srel range 500 xsize 410 ysize 12

                            hbox:
                                spacing 40
                                hbox:
                                    text "Dominance: " color "#94a3b8" size 14
                                    text "[sdom]" color "#eab308" size 14 bold True
                                hbox:
                                    text "Corruption: " color "#94a3b8" size 14
                                    text "[scorr]/100" color "#a855f7" size 14 bold True

