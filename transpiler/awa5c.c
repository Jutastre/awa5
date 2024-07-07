/* this file is just where i implemented and tested
the c code to then copy paste into the transpiler code blocks
in large part just so i could have my ide in c mode
its not meant to be used for anything on its own*/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct Bubble Bubble;

typedef union Bubble_Data Bubble_Data;

struct Bubble {
    _Bool is_double;
    union Bubble_Data {
        __int32_t numerical;
        Bubble* sub_head;
    } data;
    Bubble* next;
};

Bubble* abyss = NULL;

char AwaSCII_LOOKUP[64] = "AWawJELYHOSIUMjelyhosiumPCNTpcntBDFGRbdfgr0123456789 .,!'()~_/;\n";

size_t REVERSE_AwaSCII_LOOKUP[127] = { 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 63, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 52, 55, 56, 56, 56, 56, 56, 56, 57, 58, 56, 56, 54, 56, 53, 61, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 56, 62, 56, 56, 56, 56, 56, 0, 32, 25, 33, 5, 34, 35, 8, 11, 4, 56, 6, 13, 26, 9, 24, 56, 36, 10, 27, 12, 56, 1, 56, 7, 56, 56, 56, 56, 56, 60, 56, 2, 37, 29, 38, 15, 39, 40, 18, 21, 14, 56, 16, 23, 30, 19, 28, 56, 41, 20, 31, 22, 56, 3, 56, 17, 56, 56, 56, 56, 59 };


static inline void delete_bubble_list(Bubble* head) {
    while (head != NULL) {
        Bubble* next = head->next;
        if (head->is_double) {
            delete_bubble_list(head->data.sub_head);
        }
        free(head);
        head = next;
    }
}

static inline void delete_top_bubble(Bubble** abyss) {
    Bubble* to_delete = *abyss;
    if (to_delete->is_double) {
        delete_bubble_list(to_delete->data.sub_head);
    }
    *abyss = to_delete->next;
    free(to_delete);
}

static inline void Awa_01_recursive_helper(Bubble** abyss) {
    if ((*abyss)->is_double) {
        for (Bubble* cur = (*abyss)->data.sub_head; cur != NULL; cur = cur->next) {
            Awa_01_recursive_helper(&cur);
        }
    }
    else {
        printf("%c", AwaSCII_LOOKUP[(*abyss)->data.numerical]);
    }
}
static inline void Awa_01_print(Bubble** abyss) {
    Awa_01_recursive_helper(abyss);
    delete_top_bubble(abyss);
}

static inline void Awa_02_recursive_helper(Bubble** abyss) {
    if ((*abyss)->is_double) {
        for (Bubble* cur = (*abyss)->data.sub_head; cur != NULL; cur = cur->next) {
            Awa_02_recursive_helper(&cur);
            if (cur->next != NULL) {
                printf(" ");
            }
        }
    }
    else {
        printf("%i", (*abyss)->data.numerical);
    }
}
static inline void Awa_02_print_num(Bubble** abyss) {
    Awa_02_recursive_helper(abyss);
    delete_top_bubble(abyss);
}

static inline void Awa_05_blow(Bubble** abyss, int value); //declare in advance so it can be referenced in 3 and 4

static inline void Awa_03_blow_input_string(Bubble** abyss) {
    char input_buffer[128];
    scanf("%127s", input_buffer);
    for (int idx = 0; input_buffer[idx] != 0; idx++) {
        Awa_05_blow(abyss, REVERSE_AwaSCII_LOOKUP[input_buffer[idx]]);
    }
}
static inline void Awa_03_blow_input_string_with_argparse(Bubble** abyss, size_t* argc, char** argv, size_t* args_consumed) {
    char input_buffer[128];
    char* input_buffer_ptr;
    if (*args_consumed < *argc) {
        input_buffer_ptr = argv[*args_consumed];
    }
    else {
        input_buffer_ptr = input_buffer;
    }
    scanf("%127s", input_buffer_ptr);
    for (int idx = 0; input_buffer_ptr[idx] != 0; idx++) {
        Awa_05_blow(abyss, REVERSE_AwaSCII_LOOKUP[input_buffer_ptr[idx]]);
    }
}

static inline void Awa_04_blow_input_number(Bubble** abyss) {
    __int32_t input_buffer;
    scanf("%i", &input_buffer);

    Awa_05_blow(abyss, input_buffer);
}

static inline void Awa_04_blow_input_number_with_argparse(Bubble** abyss, size_t* argc, char** argv, size_t* args_consumed) {
    if (*args_consumed < *argc) {
        Awa_05_blow(abyss, atoi(argv[*args_consumed]));
        *args_consumed++;
    }
    else {
        __int32_t input_buffer;
        scanf("%i", &input_buffer);

        Awa_05_blow(abyss, input_buffer);
    }
}

static inline void Awa_05_blow(Bubble** abyss, int value) {
    Bubble* new_bubble = malloc(sizeof(Bubble));
    new_bubble->is_double = false;
    new_bubble->next = *abyss;
    new_bubble->data.numerical = value;
    *abyss = new_bubble;
}

static inline void Awa_06_submerge(Bubble** abyss, int value) {
    Bubble* to_insert = *abyss;
    *abyss = (*abyss)->next;
    Bubble* before_insertion = *abyss;
    if (value == 0) {
        while (before_insertion->next != NULL) {
            before_insertion = before_insertion->next;
        }
    }
    else {
        for (int i = 0; i < value - 1; i++) {
            before_insertion = before_insertion->next;
        }
    }
    Bubble* after_insertion = before_insertion->next;
    before_insertion->next = to_insert;
    to_insert->next = after_insertion;
}

static inline void Awa_07_pop(Bubble** abyss) {
    Bubble* sub_head;
    if ((*abyss)->is_double) {
        sub_head = (*abyss)->data.sub_head;
        Bubble* sub_tail = sub_head;
        while (sub_tail->next != NULL) {
            sub_tail = sub_tail->next;
        }
        sub_tail->next = (*abyss)->next;
    }
    else {
        sub_head = (*abyss)->next;
    }
    free(*abyss);
    *abyss = sub_head;
}

static inline Bubble* _recursive_duplication_helper(Bubble* old_head) {
    Bubble* new_head = malloc(sizeof(Bubble));
    if (old_head->is_double) {
        new_head->data.sub_head = _recursive_duplication_helper(old_head->data.sub_head);
    }
    else {
        new_head->data = old_head->data;
    }
    new_head->is_double = old_head->is_double;
    Bubble* traversal = old_head;
    Bubble* new_tail = new_head;
    while (traversal->next != NULL) {
        traversal = traversal->next;
        new_tail->next = malloc(sizeof(Bubble));
        new_tail = new_tail->next;
        new_tail->is_double = traversal->is_double;

        if (traversal->is_double) {
            new_tail->data.sub_head = _recursive_duplication_helper(traversal->data.sub_head);
        }
        else {
            new_tail->data = traversal->data;
        }
    }
    new_tail->next = NULL;
    return new_head;
}

static inline void Awa_08_duplicate(Bubble** abyss) {
    Bubble* new_bubble = malloc(sizeof(Bubble));
    if ((*abyss)->is_double) {
        new_bubble->data.sub_head = _recursive_duplication_helper((*abyss)->data.sub_head);
    }
    else {
        new_bubble->data = (*abyss)->data;
    }
    new_bubble->is_double = (*abyss)->is_double;
    new_bubble->next = (*abyss);
    (*abyss) = new_bubble;
}

static inline void Awa_09_surround(Bubble** abyss, int value) {
    Bubble* old_head = *abyss;
    Bubble* new_head = *abyss;

    for (int i = 0; i < value - 1; i++) {
        new_head = (new_head)->next;
    }

    Bubble* new_tail = new_head;
    new_head = (new_head)->next;
    new_tail->next = NULL;

    Bubble* new_bubble = malloc(sizeof(Bubble));
    new_bubble->is_double = true;
    new_bubble->next = new_head;
    new_bubble->data.sub_head = old_head;
    *abyss = new_bubble;
}

static inline void Awa_0A_merge_no_add(Bubble** abyss) {
    Bubble* bubble1 = (*abyss);
    Bubble* bubble2 = (*abyss)->next;

    if (bubble1->is_double && bubble2->is_double) { // both double
        Bubble* traverse = bubble1->data.sub_head;
        while (traverse->next != NULL) {
            traverse = traverse->next;
        }
        traverse->next = bubble2->data.sub_head;
        bubble1->next = bubble2->next;
        free(bubble2);
    }
    else if (bubble1->is_double && !bubble2->is_double) { // 1 double
        Bubble* traverse = bubble1->data.sub_head;
        while (traverse->next != NULL) {
            traverse = traverse->next;
        }
        traverse->next = bubble2;
        bubble1->next = bubble2->next;
        bubble2->next = NULL;
    }
    else if (!bubble1->is_double && bubble2->is_double) { // 2 double

        bubble1->next = bubble2->data.sub_head;
        bubble2->data.sub_head = bubble1;
        *abyss = bubble2;
    }
    else {  // both simple bubbles
        Awa_09_surround(abyss, 2);
    }
}

static inline void Awa_0A_merge(Bubble** abyss) {
    Bubble* bubble1 = (*abyss);
    Bubble* bubble2 = (*abyss)->next;

    if (bubble1->is_double && bubble2->is_double) { // both double
        Bubble* traverse = bubble1->data.sub_head;
        while (traverse->next != NULL) {
            traverse = traverse->next;
        }
        traverse->next = bubble2->data.sub_head;
        bubble1->next = bubble2->next;
        free(bubble2);
    }
    else if (bubble1->is_double && !bubble2->is_double) { // 1 double
        Bubble* traverse = bubble1->data.sub_head;
        while (traverse->next != NULL) {
            traverse = traverse->next;
        }
        traverse->next = bubble2;
        bubble1->next = bubble2->next;
        bubble2->next = NULL;
    }
    else if (!bubble1->is_double && bubble2->is_double) { // 2 double

        bubble1->next = bubble2->data.sub_head;
        bubble2->data.sub_head = bubble1;
        *abyss = bubble2;
    }
    else {  // both simple bubbles
        bubble2->data.numerical = bubble1->data.numerical + bubble2->data.numerical;
        free(bubble1);
        (*abyss) = bubble2;
    }
}

static inline void Awa_0B_add_recursive_helper_one_simple(Bubble** head_ptr, __int32_t simple_value) {
    Bubble* current = *head_ptr;
    while (current != NULL) {
        if (current->is_double) {
            Awa_0B_add_recursive_helper_one_simple(&(current->data.sub_head), simple_value);
        }
        else {
            current->data.numerical += simple_value;
        }
        current = current->next;
    }
}

static inline void Awa_0B_add_recursive_helper_both_double(Bubble*bubble1, Bubble*bubble2) {
    //this kills the bubble(2)
    Bubble* current1 = bubble1->data.sub_head;
    Bubble* current2 = bubble2->data.sub_head;
    if (bubble2->data.sub_head == NULL){
        //free(bubble2);
        return;
    }
    else if (bubble1->data.sub_head == NULL){
        bubble1->data.sub_head = bubble2->data.sub_head;
        //free(bubble2);
        bubble2->data.sub_head = NULL;
        return;
    }
    while (current1 != NULL && current2 != NULL) {

        if (!current1->is_double && !current2->is_double) { // both simple
            current1->data.numerical += current2->data.numerical;
        }
        else if (current1->is_double != current2->is_double) { // 1 double
            __int32_t simple_value;

            //excise the simple
            if (current1->is_double) {
                simple_value = current2->data.numerical;
            }
            else {
                simple_value = current1->data.numerical;

                //move contents from bubble2 to bubble1:
                current1->data.sub_head = current2->data.sub_head;
                current1->is_double = true;
                current2->is_double = false;
                current2->data.sub_head = NULL; //can i skip this line? pretty sure i can, it wont be assumed to be a pointer ever since is_double is false
            }
            Awa_0B_add_recursive_helper_one_simple(&(current1->data.sub_head), simple_value);
        }
        else {  // both double
            Awa_0B_add_recursive_helper_both_double(bubble1,bubble2);
        }
    }
    //traverse AGAIN to find tail and make sure its on b1
    current1 = bubble1->data.sub_head;
    current2 = bubble2->data.sub_head;
    while (current1->next != NULL && current2->next != NULL) {
        current1 = current1->next;
        current2 = current2->next;
    }
    //transfer tail if its on 2
    if (current1->next == NULL){
        current1->next = current2->next;
        current2->next = NULL;
    }
}
static inline void Awa_0B_add(Bubble** abyss) {
    Bubble* bubble1 = (*abyss);
    Bubble* bubble2 = (*abyss)->next;

    if (!bubble1->is_double && !bubble2->is_double) { // both simple
        bubble2->data.numerical = bubble1->data.numerical + bubble2->data.numerical;
        free(bubble1);
        (*abyss) = bubble2;
    }
    else if (bubble1->is_double != bubble2->is_double) { // 1 double
        __int32_t simple_value;

        //excise the simple
        if (bubble1->is_double) {
            simple_value = bubble2->data.numerical;
            bubble1->next = bubble2->next;
            free(bubble2);
        }
        else {
            simple_value = bubble1->data.numerical;
            (*abyss) = bubble2;
            free(bubble1);
        }
        Awa_0B_add_recursive_helper_one_simple(&((*abyss)->data.sub_head), simple_value);
    }
    else {  // both double
        Awa_0B_add_recursive_helper_both_double(bubble1,bubble2);
        bubble1->next = bubble2->next;
        delete_bubble_list(bubble2->data.sub_head);
        free(bubble2);
    }
}


static inline void Awa_0C_sub_recursive_helper_one_simple(Bubble** head_ptr, __int32_t simple_value, _Bool reversed) {
    Bubble* current = *head_ptr;
    while (current != NULL) {
        if (current->is_double) {
            Awa_0C_sub_recursive_helper_one_simple(&(current->data.sub_head), simple_value, reversed);
        }
        else {
            if (!reversed) {
                current->data.numerical -= simple_value;
            }
            else {
                current->data.numerical = simple_value - current->data.numerical;
            }
        }
        current = current->next;
    }
}


static inline void Awa_0C_sub_recursive_helper_both_double(Bubble*bubble1, Bubble*bubble2) {
    //this kills the bubble(2)
    Bubble* current1 = bubble1->data.sub_head;
    Bubble* current2 = bubble2->data.sub_head;
    if (bubble2->data.sub_head == NULL){
        //free(bubble2);
        return;
    }
    else if (bubble1->data.sub_head == NULL){
        bubble1->data.sub_head = bubble2->data.sub_head;
        //free(bubble2);
        bubble2->data.sub_head = NULL;
        return;
    }
    while (current1 != NULL && current2 != NULL) {

        if (!current1->is_double && !current2->is_double) { // both simple
            current1->data.numerical -= current2->data.numerical;
        }
        else if (current1->is_double != current2->is_double) { // 1 double
            __int32_t simple_value;
            _Bool reversed;

            //excise the simple
            if (current1->is_double) {
                simple_value = current2->data.numerical;
                reversed = false;
            }
            else {
                simple_value = current1->data.numerical;
                reversed = true;

                //move contents from bubble2 to bubble1:
                current1->data.sub_head = current2->data.sub_head;
                current1->is_double = true;
                current2->is_double = false;
                current2->data.sub_head = NULL; //can i skip this line? pretty sure i can, it wont be assumed to be a pointer ever since is_double is false
            }
            Awa_0C_sub_recursive_helper_one_simple(&(current1->data.sub_head), simple_value, reversed);
        }
        else {  // both double
            Awa_0C_sub_recursive_helper_both_double(bubble1,bubble2);
        }
    }
    //traverse AGAIN to find tail and make sure its on b1
    current1 = bubble1->data.sub_head;
    current2 = bubble2->data.sub_head;
    while (current1->next != NULL && current2->next != NULL) {
        current1 = current1->next;
        current2 = current2->next;
    }
    //transfer tail if its on 2
    if (current1->next == NULL){
        current1->next = current2->next;
        current2->next = NULL;
    }
}


static inline void Awa_0C_sub(Bubble** abyss) {
    Bubble* bubble1 = (*abyss);
    Bubble* bubble2 = (*abyss)->next;

    if (!bubble1->is_double && !bubble2->is_double) { // both simple
        bubble2->data.numerical = bubble1->data.numerical - bubble2->data.numerical;
        free(bubble1);
        (*abyss) = bubble2;
    }
    else if (bubble1->is_double != bubble2->is_double) { // 1 double
        __int32_t simple_value;
        _Bool reversed;

        //excise the simple
        if (bubble1->is_double) {
            simple_value = bubble2->data.numerical;
            bubble1->next = bubble2->next;
            free(bubble2);
            reversed = false;
        }
        else {
            simple_value = bubble1->data.numerical; 
            (*abyss) = bubble2;
            free(bubble1);
            reversed = true;
        }
        Awa_0C_sub_recursive_helper_one_simple(&((*abyss)->data.sub_head), simple_value, reversed);
    }
    else {  // both double
        Awa_0C_sub_recursive_helper_both_double(bubble1,bubble2);
        bubble1->next = bubble2->next;
        delete_bubble_list(bubble2->data.sub_head);
        free(bubble2);
    }
}

static inline void Awa_0D_mul_recursive_helper_one_simple(Bubble** head_ptr, __int32_t simple_value) {
    Bubble* current = *head_ptr;
    while (current != NULL) {
        if (current->is_double) {
            Awa_0D_mul_recursive_helper_one_simple(&(current->data.sub_head), simple_value);
        }
        else {
            current->data.numerical *= simple_value;
        }
        current = current->next;
    }
}

static inline void Awa_0D_mul_recursive_helper_both_double(Bubble*bubble1, Bubble*bubble2) {
    //this kills the bubble(2)
    Bubble* current1 = bubble1->data.sub_head;
    Bubble* current2 = bubble2->data.sub_head;
    if (bubble2->data.sub_head == NULL){
        //free(bubble2);
        return;
    }
    else if (bubble1->data.sub_head == NULL){
        bubble1->data.sub_head = bubble2->data.sub_head;
        //free(bubble2);
        bubble2->data.sub_head = NULL;
        return;
    }
    while (current1 != NULL && current2 != NULL) {

        if (!current1->is_double && !current2->is_double) { // both simple
            current1->data.numerical *= current2->data.numerical;
        }
        else if (current1->is_double != current2->is_double) { // 1 double
            __int32_t simple_value;

            //excise the simple
            if (current1->is_double) {
                simple_value = current2->data.numerical;
            }
            else {
                simple_value = current1->data.numerical;

                //move contents from bubble2 to bubble1:
                current1->data.sub_head = current2->data.sub_head;
                current1->is_double = true;
                current2->is_double = false;
                current2->data.sub_head = NULL; //can i skip this line? pretty sure i can, it wont be assumed to be a pointer ever since is_double is false
            }
            Awa_0D_mul_recursive_helper_one_simple(&(current1->data.sub_head), simple_value);
        }
        else {  // both double
            Awa_0D_mul_recursive_helper_both_double(bubble1,bubble2);
        }
    }
    //traverse AGAIN to find tail and make sure its on b1
    current1 = bubble1->data.sub_head;
    current2 = bubble2->data.sub_head;
    while (current1->next != NULL && current2->next != NULL) {
        current1 = current1->next;
        current2 = current2->next;
    }
    //transfer tail if its on 2
    if (current1->next == NULL){
        current1->next = current2->next;
        current2->next = NULL;
    }
}

static inline void Awa_0D_mul(Bubble** abyss) {
    Bubble* bubble1 = (*abyss);
    Bubble* bubble2 = (*abyss)->next;

    if (!bubble1->is_double && !bubble2->is_double) { // both simple
        bubble2->data.numerical = bubble1->data.numerical * bubble2->data.numerical;
        free(bubble1);
        (*abyss) = bubble2;
    }
    else if (bubble1->is_double != bubble2->is_double) { // 1 double
        __int32_t simple_value;

        //excise the simple
        if (bubble1->is_double) {
            simple_value = bubble2->data.numerical;
            bubble1->next = bubble2->next;
            free(bubble2);
        }
        else {
            simple_value = bubble1->data.numerical;
            (*abyss) = bubble2;
            free(bubble1);
        }
        Awa_0D_mul_recursive_helper_one_simple(&((*abyss)->data.sub_head), simple_value);
    }
    else {  // both double
        Awa_0D_mul_recursive_helper_both_double(bubble1,bubble2);
        bubble1->next = bubble2->next;
        delete_bubble_list(bubble2->data.sub_head);
        free(bubble2);
    }
}

static inline void Awa_0E_div_recursive_helper_one_simple(Bubble** head_ptr, __int32_t simple_value, _Bool reversed) {
    Bubble* current = *head_ptr;
    while (current != NULL) {
        if (current->is_double) {
            Awa_0E_div_recursive_helper_one_simple(&(current->data.sub_head), simple_value, reversed);
        }
        else {
            Bubble* quotient = malloc(sizeof(Bubble));
            Bubble* remainder = malloc(sizeof(Bubble));
            quotient->is_double = false;
            quotient->data.numerical = reversed ? current->data.numerical / simple_value : simple_value / current->data.numerical; 
            //yeah i used a trinary what are you gonna do about it?

            remainder->is_double = false;
            remainder->data.numerical = reversed ? current->data.numerical % simple_value : simple_value % current->data.numerical; 
            //did it again (would it be better to only do a single comparison? will the optimizer fix that for me? feel like it should)

            current->is_double = true;
            current->data.sub_head = quotient;
            quotient->next = remainder;
            remainder->next = NULL;

        }
        current = current->next;
    }
}

static inline void Awa_0E_div_recursive_helper_both_double(Bubble*bubble1, Bubble*bubble2) {
    //this kills the bubble(2)
    Bubble* current1 = bubble1->data.sub_head;
    Bubble* current2 = bubble2->data.sub_head;
    if (bubble2->data.sub_head == NULL){
        //free(bubble2);
        return;
    }
    else if (bubble1->data.sub_head == NULL){
        bubble1->data.sub_head = bubble2->data.sub_head;
        bubble2->data.sub_head = NULL;
        //free(bubble2);
        return;
    }
    while (current1 != NULL && current2 != NULL) {

        if (!current1->is_double && !current2->is_double) { // both simple
            int number1 = current1->data.numerical;
            int number2 = current2->data.numerical;
            Bubble * new_bubble1 = malloc(sizeof(Bubble));
            Bubble * new_bubble2 = malloc(sizeof(Bubble));
            new_bubble1->data.numerical = number1 / number2;
            new_bubble2->data.numerical = number1 % number2;
            new_bubble1->is_double = false;
            new_bubble2->is_double = false;
            new_bubble1->next = new_bubble2;
            new_bubble2->next = NULL;

            current1->is_double = true;
            current1->data.sub_head = new_bubble1;
        }
        else if (current1->is_double != current2->is_double) { // 1 double
            __int32_t simple_value;
            _Bool reversed;

            //excise the simple
            if (current1->is_double) {
                simple_value = current2->data.numerical;
                reversed = false;
            }
            else {
                simple_value = current1->data.numerical;
                reversed = true;

                //move contents from bubble2 to bubble1:
                current1->data.sub_head = current2->data.sub_head;
                current1->is_double = true;
                current2->is_double = false;
                current2->data.sub_head = NULL; //can i skip this line? pretty sure i can, it wont be assumed to be a pointer ever since is_double is false
            }
            Awa_0E_div_recursive_helper_one_simple(&(current1->data.sub_head), simple_value, reversed);
        }
        else {  // both double
            Awa_0E_div_recursive_helper_both_double(bubble1,bubble2);
        }
    }
    //traverse AGAIN to find tail and make sure its on b1
    current1 = bubble1->data.sub_head;
    current2 = bubble2->data.sub_head;
    while (current1->next != NULL && current2->next != NULL) {
        current1 = current1->next;
        current2 = current2->next;
    }
    //transfer tail if its on 2
    if (current1->next == NULL){
        current1->next = current2->next;
        current2->next = NULL;
    }
}

static inline void Awa_0E_div(Bubble** abyss) {
    Bubble* bubble1 = (*abyss);
    Bubble* bubble2 = (*abyss)->next;

    if (!bubble1->is_double && !bubble2->is_double) { // both simple
        int number1 = bubble1->data.numerical;
        int number2 = bubble2->data.numerical;
        bubble1->data.numerical = number1 / number2;
        bubble2->data.numerical = number1 % number2;
        Awa_09_surround(abyss, 2);
    }
    else if (bubble1->is_double != bubble2->is_double) { // 1 double
        __int32_t simple_value;
        _Bool reversed;

        //excise the simple
        if (bubble1->is_double) {
            simple_value = bubble2->data.numerical;
            bubble1->next = bubble2->next;
            free(bubble2);
            reversed = false;
        }
        else {
            simple_value = bubble1->data.numerical;
            (*abyss) = bubble2;
            free(bubble1);
            reversed = true;
        }
        Awa_0E_div_recursive_helper_one_simple(&((*abyss)->data.sub_head), simple_value, reversed);
    }
    else {  // both double
        Awa_0E_div_recursive_helper_both_double(bubble1,bubble2);
        bubble1->next = bubble2->next;
        delete_bubble_list(bubble2->data.sub_head);
        free(bubble2);
    }
}



static inline _Bool Awa_12_equal(Bubble** abyss) {
    return ((*abyss)->data.numerical == (*abyss)->next->data.numerical);
}

static inline _Bool Awa_13_greater_than(Bubble** abyss) {
    return ((*abyss)->data.numerical > (*abyss)->next->data.numerical);
}

static inline _Bool Awa_14_less_than(Bubble** abyss) {
    return ((*abyss)->data.numerical < (*abyss)->next->data.numerical);
}

static inline void Awa_0F_count(Bubble** abyss) {
    int count = 0;
    if (!(*abyss)->is_double) {
        Awa_05_blow(abyss, 0); //blows a zero on simple bubble
        return;
    }
    Bubble* bubble = (*abyss)->data.sub_head;
    while (bubble != NULL) {
        bubble = bubble->next;
        count++;
    }
    Awa_05_blow(abyss, count);
}

int main() {

    Awa_05_blow(&abyss, 3);
    Awa_05_blow(&abyss, 2);
    Awa_05_blow(&abyss, 1);
    Awa_02_print_num(&abyss);
    Awa_02_print_num(&abyss);
    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 63);
    Awa_01_print(&abyss); //should print 123\n

    Awa_05_blow(&abyss, 3);
    Awa_05_blow(&abyss, 2);
    Awa_05_blow(&abyss, 1);
    Awa_09_surround(&abyss, 3);
    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 63);
    Awa_01_print(&abyss); //should print 1 2 3\n

    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 1);
    Awa_06_submerge(&abyss, 2);
    Awa_09_surround(&abyss, 5);
    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 63);
    Awa_01_print(&abyss); //should print 5 5 1 5 5 \n

    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 1);
    Awa_06_submerge(&abyss, 0);
    Awa_09_surround(&abyss, 5);
    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 63);
    Awa_01_print(&abyss); //should print 5 5 5 5 1\n

    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 1);
    Awa_06_submerge(&abyss, 0);
    Awa_09_surround(&abyss, 5);
    Awa_0F_count(&abyss);
    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 63);
    Awa_01_print(&abyss); //should print 5\n

    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 63);
    Awa_01_print(&abyss); //should print 5 5 5 5 1\n

    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 5);
    Awa_05_blow(&abyss, 1);
    Awa_09_surround(&abyss, 3);
    Awa_08_duplicate(&abyss);
    Awa_02_print_num(&abyss);
    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 63);
    Awa_01_print(&abyss); //should print 1 5 51 5 5\n


    Awa_05_blow(&abyss, 2);
    Awa_05_blow(&abyss, 7);
    Awa_0B_add(&abyss);
    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 2);
    Awa_05_blow(&abyss, 7);
    Awa_0C_sub(&abyss);
    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 2);
    Awa_05_blow(&abyss, 7);
    Awa_0D_mul(&abyss);
    Awa_02_print_num(&abyss);

    Awa_05_blow(&abyss, 2);
    Awa_05_blow(&abyss, 7);
    Awa_0E_div(&abyss);
    Awa_02_print_num(&abyss);

    //Awa_04_blow_input_number(&abyss);
    Awa_05_blow(&abyss, 999);
    Awa_05_blow(&abyss, 1);
lbl_0:
    if (Awa_12_equal(&abyss)) {
        goto lbl_2;
    }
    Awa_06_submerge(&abyss, 1);
    Awa_08_duplicate(&abyss);
    Awa_06_submerge(&abyss, 2);
    Awa_06_submerge(&abyss, 1);
    Awa_05_blow(&abyss, 1);
    Awa_0B_add(&abyss);
    Awa_08_duplicate(&abyss);
    Awa_06_submerge(&abyss, 2);
lbl_1:
    Awa_06_submerge(&abyss, 1);
    Awa_0E_div(&abyss);
    Awa_07_pop(&abyss);
    Awa_07_pop(&abyss);
    Awa_05_blow(&abyss, 0);
    if (Awa_12_equal(&abyss)) {
        goto lbl_3;
    }
    Awa_07_pop(&abyss);
    Awa_07_pop(&abyss);
    goto lbl_0;
lbl_2:
    return 0;
lbl_3:
    Awa_07_pop(&abyss);
    Awa_07_pop(&abyss);
    Awa_08_duplicate(&abyss);
    Awa_05_blow(&abyss, 34);
    Awa_01_print(&abyss);
    Awa_05_blow(&abyss, 2);
    Awa_01_print(&abyss);
    Awa_05_blow(&abyss, 29);
    Awa_01_print(&abyss);
    Awa_05_blow(&abyss, 31);
    Awa_01_print(&abyss);
    Awa_05_blow(&abyss, 19);
    Awa_01_print(&abyss);
    Awa_05_blow(&abyss, 41);
    Awa_01_print(&abyss);
    Awa_05_blow(&abyss, 62);
    Awa_01_print(&abyss);
    Awa_05_blow(&abyss, 52);
    Awa_01_print(&abyss);
    Awa_02_print_num(&abyss);
    Awa_05_blow(&abyss, 63);
    Awa_01_print(&abyss);
    goto lbl_0;


    return 0;
}