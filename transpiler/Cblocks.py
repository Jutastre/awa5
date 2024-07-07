dependencies = {}
c_functions:dict[int:str] = {}
c_code = {}

boilerplate = """#include <stdio.h>
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
"""

awascii_lookup = """char AwaSCII_LOOKUP[64] = "AWawJELYHOSIUMjelyhosiumPCNTpcntBDFGRbdfgr0123456789 .,!'()~_/;\\n";
"""

reverse_awascii_lookup = """size_t REVERSE_AwaSCII_LOOKUP[127] = {56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 63, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 56, 52, 55, 56, 56, 56, 56, 56, 56, 57, 58, 56, 56, 54, 56, 53, 61, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 56, 62, 56, 56, 56, 56, 56, 0, 32, 25, 33, 5, 34, 35, 8, 11, 4, 56, 6, 13, 26, 9, 24, 56, 36, 10, 27, 12, 56, 1, 56, 7, 56, 56, 56, 56, 56, 60, 56, 2, 37, 29, 38, 15, 39, 40, 18, 21, 14, 56, 16, 23, 30, 19, 28, 56, 41, 20, 31, 22, 56, 3, 56, 17, 56, 56, 56, 56, 59};
"""

c_functions["delete"] = """static inline void delete_bubble_list(Bubble* head) {
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
"""

dependencies[0x01] =('delete','awascii_lookup',)

c_functions[0x01] = """static inline void Awa_01_recursive_helper(Bubble** abyss) {
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
"""

c_code[0x01] = """Awa_01_print(&abyss);
"""

dependencies[0x02] =('delete',)

c_functions[0x02] = """static inline void Awa_02_recursive_helper(Bubble** abyss) {
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
"""

c_code[0x02] = """Awa_02_print_num(&abyss);
"""

dependencies[0x03] =('reverse_awascii_lookup',0x05,)

c_functions[0x03] = """static inline void Awa_03_blow_input_string(Bubble** abyss) {
    char input_buffer[128];
    scanf("%127s", input_buffer);
    for (int idx = 0; input_buffer[idx] != 0; idx++) {
        Awa_05_blow(abyss, REVERSE_AwaSCII_LOOKUP[input_buffer[idx]]);
    }
}
"""

c_functions["0x03 argparse"] = """static inline void Awa_03_blow_input_string(Bubble** abyss, int argc, char** argv, size_t * args_consumed) {
    char input_buffer[128];
    char *input_buffer_ptr;
    if (*args_consumed < argc) {
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

"""

c_code[0x03] = """Awa_03_blow_input_string(&abyss);
"""

c_code["0x03 argparse"] = """Awa_03_blow_input_string(&abyss, argc, argv, &args_consumed);
"""

dependencies[0x04] =(0x05,)

c_functions[0x04] = """static inline void Awa_04_blow_input_number(Bubble** abyss) {
    __int32_t input_buffer;
    if (scanf("%i", &input_buffer)) {
        Awa_05_blow(abyss, input_buffer);
    }
}
"""

c_functions["0x04 argparse"] = """static inline void Awa_04_blow_input_number(Bubble** abyss, int argc, char** argv, size_t * args_consumed) {
    if (*args_consumed < argc) {
        Awa_05_blow(abyss, atoi(argv[*args_consumed]));
        *args_consumed++;
    }
    else {
        __int32_t input_buffer;
        if (scanf("%i", &input_buffer)) {
            Awa_05_blow(abyss, input_buffer);
        }
    }
}

"""

c_code[0x04] = """Awa_04_blow_input_number(&abyss);
"""

c_code["0x04 argparse"] = """Awa_04_blow_input_number(&abyss, argc, argv, &args_consumed);
"""

c_functions[0x05] = """static inline void Awa_05_blow(Bubble** abyss, int value) {
    Bubble* new_bubble = malloc(sizeof(Bubble));
    new_bubble->is_double = false;
    new_bubble->next = *abyss;
    new_bubble->data.numerical = value;
    *abyss = new_bubble;
}
"""

c_code[0x05] = """Awa_05_blow(&abyss, %FUNCTION_PARAMETER%);
"""

c_functions[0x06] = """static inline void Awa_06_submerge(Bubble** abyss, int value) {
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
"""

c_code[0x06] = """Awa_06_submerge(&abyss, %FUNCTION_PARAMETER%);
"""

c_functions[0x07] = """static inline void Awa_07_pop(Bubble** abyss) {
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
"""

c_code[0x07] = """Awa_07_pop(&abyss);
"""



c_functions[0x08] = """static inline Bubble* _recursive_duplication_helper(Bubble* old_head) {
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
        new_tail->is_double = traversal->is_double;
        new_tail = new_tail->next;
        
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
"""

c_code[0x08] = """Awa_08_duplicate(&abyss);
"""


c_functions[0x09] = """static inline void Awa_09_surround(Bubble** abyss, int value) {
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
"""

c_code[0x09] = """Awa_09_surround(&abyss, %FUNCTION_PARAMETER%);
"""

c_functions[0x0A] = """static inline void Awa_0A_merge(Bubble** abyss) {
    Bubble * bubble1 = (*abyss);
    Bubble * bubble2 = (*abyss)->next;

    if (bubble1->is_double && bubble2->is_double) { // both double
        Bubble * traverse = bubble1->data.sub_head;
        while (traverse->next != NULL) {
            traverse = traverse->next;
        }
        traverse->next = bubble2->data.sub_head;
        bubble1->next = bubble2->next;
        free(bubble2);
    }
    else if (bubble1->is_double && !bubble2->is_double) { // 1 double
        Bubble * traverse = bubble1->data.sub_head;
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
"""

dependencies["alternative 0x0A"] = (0x09,)

c_functions["alternative 0x0A"] = """static inline void Awa_0A_merge(Bubble** abyss) {
    Bubble * bubble1 = (*abyss);
    Bubble * bubble2 = (*abyss)->next;

    if (bubble1->is_double && bubble2->is_double) { // both double
        Bubble * traverse = bubble1->data.sub_head;
        while (traverse->next != NULL) {
            traverse = traverse->next;
        }
        traverse->next = bubble2->data.sub_head;
        bubble1->next = bubble2->next;
        free(bubble2);
    }
    else if (bubble1->is_double && !bubble2->is_double) { // 1 double
        Bubble * traverse = bubble1->data.sub_head;
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
"""

c_code[0x0A] = """Awa_0A_merge(&abyss);
"""



c_functions[0x0B] = """static inline void Awa_0B_recursive_helper_one_simple(Bubble** head_ptr, __int32_t simple_value) {
    Bubble * current = *head_ptr;
    while (current != NULL) {
        if (current->is_double) {
            Awa_0B_recursive_helper_one_simple(&(current->data.sub_head), simple_value);
        }
        else {
            current->data.numerical += simple_value;
        }
        current = current->next;
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
        Awa_0B_recursive_helper_one_simple(&((*abyss)->data.sub_head), simple_value);
    }
    else {  // both double
        // NOT IMPLEMENTED
    }
}
"""

c_code[0x0B] = """Awa_0B_add(&abyss);
"""


c_functions[0x0C] = """static inline void Awa_0C_recursive_helper_one_simple(Bubble** head_ptr, __int32_t simple_value) {
    Bubble * current = *head_ptr;
    while (current != NULL) {
        if (current->is_double) {
            Awa_0C_recursive_helper_one_simple(&(current->data.sub_head), simple_value);
        }
        else {
            current->data.numerical -= simple_value;
        }
        current = current->next;
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
        Awa_0C_recursive_helper_one_simple(&((*abyss)->data.sub_head), simple_value);
    }
    else {  // both double
        // NOT IMPLEMENTED
    }
}
"""

c_code[0x0C] = """Awa_0C_sub(&abyss);
"""


c_functions[0x0D] = """static inline void Awa_0D_recursive_helper_one_simple(Bubble** head_ptr, __int32_t simple_value) {
    Bubble * current = *head_ptr;
    while (current != NULL) {
        if (current->is_double) {
            Awa_0D_recursive_helper_one_simple(&(current->data.sub_head), simple_value);
        }
        else {
            current->data.numerical *= simple_value;
        }
        current = current->next;
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
        Awa_0D_recursive_helper_one_simple(&((*abyss)->data.sub_head), simple_value);
    }
    else {  // both double
        // NOT IMPLEMENTED
    }
}
"""

c_code[0x0D] = """Awa_0D_mul(&abyss);
"""

dependencies[0x0E] = (0x09,)

c_functions[0x0E] = """static inline void Awa_0E_recursive_helper_one_simple(Bubble** head_ptr, __int32_t simple_value) {
    Bubble * current = *head_ptr;
    while (current != NULL) {
        if (current->is_double) {
            Awa_0E_recursive_helper_one_simple(&(current->data.sub_head), simple_value);
        }
        else {
            current->data.numerical /= simple_value; //TO BE FIXED
        }
        current = current->next;
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
        Awa_0E_recursive_helper_one_simple(&((*abyss)->data.sub_head), simple_value);
    }
    else {  // both double
        // NOT IMPLEMENTED
    }
}
"""

c_code[0x0E] = """Awa_0E_div(&abyss);
"""










c_functions[0x0F] = """static inline void Awa_0F_count(Bubble** abyss) {
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
"""

c_code[0x0F] = """Awa_0F_count(&abyss);
"""

c_functions[0x12] = """static inline _Bool Awa_12_equal(Bubble** abyss) {
    return ((*abyss)->data.numerical == (*abyss)->next->data.numerical);
}"""

c_code[0x12] = """if (Awa_12_equal(&abyss)) {
"""

c_functions[0x13] = """static inline _Bool Awa_13_greater_than(Bubble** abyss) {
    return ((*abyss)->data.numerical > (*abyss)->next->data.numerical);
}
"""

c_code[0x13] = """if (Awa_13_greater_than(&abyss)) {
"""

c_functions[0x14] = """static inline _Bool Awa_14_less_than(Bubble** abyss) {
    return ((*abyss)->data.numerical < (*abyss)->next->data.numerical);
}
"""

c_code[0x14] = """if (Awa_14_less_than(&abyss)) {
"""

c_code["print_string"] = """printf("%FUNCTION_PARAMETER%");
"""