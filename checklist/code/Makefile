
INC =-I ./inc
OUTFILE =./obj

CHECKLIST_OBJ_NEED= $(OUTFILE)/main.o $(OUTFILE)/file_operate.o $(OUTFILE)/path_analyse.o

VPATH=inc obj

checklist : $(CHECKLIST_OBJ_NEED)
	gcc $(INC) $^ -o ../checklist

#$(OUTFILE)%.o : %c 
#	gcc $(INC) -c $< $@

$(OUTFILE)/main.o : main.c
	gcc $(INC) -c $< -o $@
$(OUTFILE)/file_operate.o : file_operate.c
	gcc $(INC) -c $< -o $@
$(OUTFILE)/path_analyse.o: path_analyse.c
	gcc $(INC) -c $< -o $@




.PHONY: clean
clean: 
	-rm ../checklist ./obj/*