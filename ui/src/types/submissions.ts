export interface SubmissionField {
  id: string;
  title: string;
  value: string;
}

export interface Submission {
  id: string;
  user_name: string;
  formatted_date: string;
  formatted_time: string;
  fields: SubmissionField[];
}
