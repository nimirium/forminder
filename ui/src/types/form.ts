// src/types/form.ts

export interface Form {
    id: string;
    team_id: string;
    user_id: string;
    user_name: string;
    name: string;
    fields: Array<{
        id: string;
        type: string;
        title: string;
        options: Array<string>;
    }>;
    number_of_submissions: number;
}
