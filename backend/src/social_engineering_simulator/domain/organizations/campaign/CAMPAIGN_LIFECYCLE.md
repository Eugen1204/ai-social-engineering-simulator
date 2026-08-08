### DRAFT = the first stage of the campaign formation cycle

### SCHEDULED = stage at which the user plans the time and date of the attack

### RUNNING = direct mailing of letters, generation of logs, vulnerability analysis

### CANCELLED = canceled operation

### FINISHED = end of the completed operation

### ARCHIVED = archive of all verified or canceled transactions

| FROM  | TO  | ALLOWED? | WHY?                                                                             | 
|-------|-----|----------|----------------------------------------------------------------------------------|
| DRAFT | SCHEDULLED | YES      | logically obvious                                                                
| DRAFT | RUNNING | YES      | we can start directly at the stage of drafting without specifying the time <br/> |
| DRAFT | CANCELLED | NO       | you can't cancel a draft because it doesn't have any active role                 |
| DRAFT | ARCHIVED | NO       | reason as in the previous paragraph                                              |
|SCHEDULED | DRAFT | YES      | scheduled campaign can be returned to editable state                             |
| SCHEDULED | RUNNING | YES      | logically next operation                                                         |
|SCHEDULED | CANCELLED | YES      | you can cancel a scheduled operation indicating the reason                 |       
| RUNNING | FINISHED | YES | logically determined                                                             |
| RUNNING | CANCELLED | YES | while the operation is active it can be canceled                                 |
| FINISHED | ARCHIVED | YES | after the operation is completed, it must be sent to the archive                 |