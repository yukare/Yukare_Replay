###############################################################################
##
## Yukare Replay - Tip Window System
##
## Provides a movable and closable window to display tips or objectives.
##
###############################################################################

init python:
    def show_tip(message):
        """Exibe a janela de dica com a mensagem fornecida."""
        renpy.show_screen("yukare_tip_window", message=message)
        renpy.restart_interaction()

    def hide_tip():
        """Esconde a janela de dica programaticamente."""
        renpy.hide_screen("yukare_tip_window")
        renpy.restart_interaction()

screen yukare_tip_window(message):
    zorder 150 # Garante que fique acima de quase tudo
    
    # Draggroup permite que o conteúdo seja movido
    draggroup:
        drag:
            drag_name "tip_window"
            drag_handle (0, 0, 400, 40) # Área do topo para arrastar
            xpos 0.7 ypos 0.2 # Posição inicial (canto superior direito)
            draggable True
            
            frame:
                xsize 400
                background Frame(Solid("#1a1a1ae6"), 4, 4) # Fundo escuro levemente transparente
                padding (15, 10)
                
                vbox:
                    spacing 10
                    
                    # Cabeçalho da janela (Barra de arraste visual)
                    hbox:
                        xfill True
                        text "TIP / HINT" style "yukare_gallery_label":
                            size 16
                            bold True
                            color "#FF86C2"
                        
                        # Botão de fechar (X)
                        textbutton "X":
                            action Hide("yukare_tip_window")
                            xalign 1.0
                            text_size 18
                            text_color "#f44336"
                            text_hover_color "#ffcdd2"
                    
                    # Linha divisória
                    add Solid("#444") ysize 1
                    
                    # Conteúdo da Mensagem
                    text message:
                        style "yukare_gallery_label"
                        size 18
                        line_spacing 2
                        layout "subtitle"
                        xalign 0.0
                        color "#ffffff"
